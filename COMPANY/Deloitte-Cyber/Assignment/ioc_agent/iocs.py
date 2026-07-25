"""IOC extraction and classification.

SOC analysts paste indicators in many shapes: bare values, whole sentences
("is 8.8.8.8 malicious?"), or defanged forms (hxxp://, 185.220.101[.]45).
This module refangs, extracts, and classifies without guessing: a token either
matches a strict pattern for exactly one IOC type or it is ignored.
"""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass

# Order matters during extraction: URLs are carved out first (they contain IPs
# and domains), then hashes, then IPs, then domains.
_URL_RE = re.compile(r"""https?://[^\s'"<>,()\[\]{}]+""", re.IGNORECASE)
_HASH_RE = re.compile(r"\b([a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32})\b", re.IGNORECASE)
_IPV4_RE = re.compile(r"\b((?:\d{1,3}\.){3}\d{1,3})(?::\d{1,5})?\b")
_DOMAIN_RE = re.compile(
    r"\b((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,24})\b", re.IGNORECASE
)

# Common defanging conventions, longest patterns first.
_DEFANG = [
    ("hxxps://", "https://"),
    ("hxxp://", "http://"),
    ("[://]", "://"),
    ("[.]", "."),
    ("(.)", "."),
    ("{.}", "."),
    ("[:]", ":"),
    ("[/]", "/"),
    ("[@]", "@"),
]

HASH_TYPE_BY_LEN = {32: "md5", 40: "sha1", 64: "sha256"}

_LABELS = {
    "ip": "IPv4 address",
    "domain": "domain",
    "url": "URL",
    "md5": "MD5 hash",
    "sha1": "SHA1 hash",
    "sha256": "SHA256 hash",
}


@dataclass(frozen=True)
class IOC:
    value: str
    type: str  # ip | domain | url | md5 | sha1 | sha256

    @property
    def label(self) -> str:
        return _LABELS.get(self.type, self.type)


def refang(text: str) -> str:
    """Undo common defanging so defanged IOCs are handled like live ones.

    Also drops BOM/zero-width characters that ride along when text is pasted
    from web pages or piped through Windows shells.
    """
    out = text
    for zero_width in ("\ufeff", "\u200b", "\u200c", "\u200d", "\u2060"):
        out = out.replace(zero_width, "")
    for bad, good in _DEFANG:
        out = out.replace(bad, good)
    # Catch leftover bare "hxxp"/"hxxps" tokens (e.g. "hxxps:\\" variants).
    return re.sub(r"\bhxxp(s?)\b", r"http\1", out, flags=re.IGNORECASE)


def _valid_ip(candidate: str) -> bool:
    try:
        ipaddress.IPv4Address(candidate)
        return True
    except ValueError:
        return False


def classify(token: str) -> IOC | None:
    """Classify a single token, or return None if it is not a recognisable IOC."""
    t = refang(token.strip()).strip(".,;'\"<>()[]{}")
    if not t:
        return None
    if _URL_RE.fullmatch(t):
        return IOC(t, "url")
    if _HASH_RE.fullmatch(t):
        return IOC(t.lower(), HASH_TYPE_BY_LEN[len(t)])
    m = _IPV4_RE.fullmatch(t)
    if m and _valid_ip(m.group(1)):
        return IOC(m.group(1), "ip")  # a :port suffix, if present, is dropped
    if _DOMAIN_RE.fullmatch(t):
        return IOC(t.lower(), "domain")
    return None


# Tokens that *look like* an attempted hash but have a non-MD5/SHA1/SHA256
# length (valid lengths are consumed by _HASH_RE before this runs). Requires
# at least one a-f so bare numbers (dates, phone numbers) are not flagged.
_HEXISH_RE = re.compile(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{16,70}\b", re.IGNORECASE)


def extract_with_invalid(text: str) -> tuple[list[IOC], list[str]]:
    """Extract IOCs from free text; also collect INVALID indicator candidates.

    Returns (iocs, invalid_candidates):
    - iocs: valid IOCs in order of appearance, de-duplicated. Wider patterns
      are consumed first and blanked out of the working text so narrower ones
      cannot re-match inside them (an IP inside a URL is one URL IOC, not a
      URL plus an IP).
    - invalid_candidates: tokens that look like attempted IOCs but fail
      validation (IPv4 shapes with out-of-range octets, hex strings of a
      non-hash length). These must be surfaced to the analyst as INVALID -
      never silently dropped and never confused with 'no records' results.
    """
    work = refang(text)
    found: list[tuple[int, IOC]] = []
    invalid: list[str] = []

    def consume(pattern: re.Pattern, builder) -> None:
        nonlocal work

        def _sub(m: re.Match) -> str:
            ioc = builder(m)
            if ioc is not None:
                # Blanking preserves offsets, so m.start() is the position in
                # the original text - used to restore appearance order below.
                found.append((m.start(), ioc))
            return " " * len(m.group(0))

        work = pattern.sub(_sub, work)

    def _ip_or_invalid(m: re.Match) -> IOC | None:
        if _valid_ip(m.group(1)):
            return IOC(m.group(1), "ip")
        invalid.append(m.group(1))
        return None

    consume(_URL_RE, lambda m: IOC(m.group(0).rstrip(".,;'\")]}"), "url"))
    consume(_HASH_RE, lambda m: IOC(m.group(1).lower(), HASH_TYPE_BY_LEN[len(m.group(1))]))
    consume(_IPV4_RE, _ip_or_invalid)
    consume(_DOMAIN_RE, lambda m: IOC(m.group(1).lower(), "domain"))

    # Whatever hex-ish runs survive all consumers have a wrong hash length.
    for m in _HEXISH_RE.finditer(work):
        invalid.append(m.group(0).lower())

    seen: set = set()
    unique: list[IOC] = []
    for _, ioc in sorted(found, key=lambda pair: pair[0]):
        key = (ioc.type, ioc.value)
        if key not in seen:
            seen.add(key)
            unique.append(ioc)

    seen_invalid: set = set()
    unique_invalid: list[str] = []
    for token in invalid:
        if token not in seen_invalid:
            seen_invalid.add(token)
            unique_invalid.append(token)
    return unique, unique_invalid


def extract_iocs(text: str) -> list[IOC]:
    """Extract all valid IOCs from free text (see extract_with_invalid)."""
    return extract_with_invalid(text)[0]
