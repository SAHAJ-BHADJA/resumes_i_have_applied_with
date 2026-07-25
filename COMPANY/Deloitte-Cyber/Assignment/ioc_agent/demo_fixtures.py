"""Canned API responses for offline demo mode (--demo).

Each fixture is shaped exactly like the corresponding live abuse.ch API reply,
so the entire pipeline downstream of the HTTP layer runs unmodified. Values
are representative demo data for the assignment's sample IOC list - the report
banner makes clear that demo output is canned, not live intelligence.

Any (kind, key) with no fixture falls back to the API's real "nothing found"
response shape (see feeds._DEMO_DEFAULTS) - which is how 8.8.8.8,
microsoft.com and the synthetic hash resolve to honest "no records" answers.
"""

FIXTURES = {
    # ------------------------------------------------ IP: 185.220.101.45
    ("threatfox_search", "185.220.101.45"): {
        "query_status": "ok",
        "data": [
            {
                "id": "1128873",
                "ioc": "185.220.101.45:443",
                "ioc_type": "ip:port",
                "ioc_type_desc": "ip:port combination that is used for botnet Command&control (C&C)",
                "threat_type": "botnet_cc",
                "threat_type_desc": "Indicator that identifies a botnet command&control server (C&C)",
                "malware": "win.cobalt_strike",
                "malware_printable": "Cobalt Strike",
                "malware_alias": "Agentemis,BEACON,CobaltStrike",
                "malware_malpedia": "https://malpedia.caad.fkie.fraunhofer.de/details/win.cobalt_strike",
                "confidence_level": 75,
                "first_seen": "2025-11-02 07:14:33 UTC",
                "last_seen": "2026-05-18 11:02:41 UTC",
                "reporter": "abuse_ch",
                "reference": "https://threatfox.abuse.ch/ioc/1128873/",
                "tags": ["c2", "tor-exit", "CobaltStrike"],
            }
        ],
    },
    ("urlhaus_host", "185.220.101.45"): {
        "query_status": "ok",
        "urlhaus_reference": "https://urlhaus.abuse.ch/host/185.220.101.45/",
        "host": "185.220.101.45",
        "firstseen": "2025-10-19 04:12:07 UTC",
        "url_count": "2",
        "blacklists": {"spamhaus_dbl": "not listed", "surbl": "not listed"},
        "urls": [
            {
                "id": "3411256",
                "urlhaus_reference": "https://urlhaus.abuse.ch/url/3411256/",
                "url": "http://185.220.101.45/loader/agent.exe",
                "url_status": "offline",
                "date_added": "2026-04-02 21:44:10 UTC",
                "threat": "malware_download",
                "reporter": "abuse_ch",
                "larted": "true",
                "tags": ["exe", "CobaltStrike"],
            },
            {
                "id": "3298117",
                "urlhaus_reference": "https://urlhaus.abuse.ch/url/3298117/",
                "url": "http://185.220.101.45/stage2.bin",
                "url_status": "offline",
                "date_added": "2025-12-11 03:18:55 UTC",
                "threat": "malware_download",
                "reporter": "zbetcheckin",
                "larted": "true",
                "tags": ["bin"],
            },
        ],
    },

    # ------------------------------------------- domain: emotet-c2-update.xyz
    ("threatfox_search", "emotet-c2-update.xyz"): {
        "query_status": "ok",
        "data": [
            {
                "id": "1204551",
                "ioc": "emotet-c2-update.xyz",
                "ioc_type": "domain",
                "ioc_type_desc": "Domain that is used for botnet Command&control (C&C)",
                "threat_type": "botnet_cc",
                "threat_type_desc": "Indicator that identifies a botnet command&control server (C&C)",
                "malware": "win.emotet",
                "malware_printable": "Emotet",
                "malware_alias": "Geodo,Heodo",
                "malware_malpedia": "https://malpedia.caad.fkie.fraunhofer.de/details/win.emotet",
                "confidence_level": 90,
                "first_seen": "2025-12-14 08:01:22 UTC",
                "last_seen": "2026-06-30 17:45:09 UTC",
                "reporter": "Cryptolaemus1",
                "reference": "https://threatfox.abuse.ch/ioc/1204551/",
                "tags": ["emotet", "c2", "epoch5"],
            }
        ],
    },

    # ------------------- URL: http://194.165.16.11/bins/tsunami.arm7
    ("urlhaus_url", "http://194.165.16.11/bins/tsunami.arm7"): {
        "query_status": "ok",
        "id": "105821",
        "urlhaus_reference": "https://urlhaus.abuse.ch/url/105821/",
        "url": "http://194.165.16.11/bins/tsunami.arm7",
        "url_status": "offline",
        "host": "194.165.16.11",
        "date_added": "2019-01-19 01:33:26 UTC",
        "last_online": "2019-02-04 16:02:11 UTC",
        "threat": "malware_download",
        "blacklists": {"spamhaus_dbl": "not listed", "surbl": "not listed"},
        "reporter": "zbetcheckin",
        "larted": "true",
        "tags": ["elf", "Tsunami", "arm"],
        "payloads": [
            {
                "firstseen": "2019-01-19",
                "filename": "tsunami.arm7",
                "file_type": "elf",
                "response_size": "45892",
                "response_md5": "0f6c00ad2f2e5b6b8f0d5f39c861f1f2",
                "response_sha256": "b7a1e2c4d90f3a5c6e8b1d2f4a7c9e0b3d5f7a9c1e3b5d7f9a1c3e5b7d9f1a3c",
                "signature": "Tsunami",
            }
        ],
    },

    # ---------------------------- hash: EICAR test file (MD5)
    ("mb_hash", "44d88612fea8a8f36de82e1278abb02f"): {
        "query_status": "ok",
        "data": [
            {
                "sha256_hash": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
                "sha1_hash": "3395856ce81f2b7382dee72602f798b642f14140",
                "md5_hash": "44d88612fea8a8f36de82e1278abb02f",
                "first_seen": "2020-07-24 11:29:47 UTC",
                "last_seen": None,
                "file_name": "eicar.com",
                "file_size": 68,
                "file_type_mime": "text/plain",
                "file_type": "com",
                "reporter": "abuse_ch",
                "origin_country": "CH",
                "anonymous": 0,
                "signature": None,
                "imphash": None,
                "tlsh": None,
                "ssdeep": "3:a+JraNvsgzsVqSwHq9:tJuOgzsko",
                "comment": None,
                "delivery_method": "other",
                "tags": ["eicar", "test-file"],
                "code_sign": [],
                "intelligence": {
                    "clamav": ["Win.Test.EICAR_HDB-1"],
                    "downloads": "18321",
                    "uploads": "64",
                    "mail": None,
                },
            }
        ],
    },

    # --------------------- ThreatFox recent IOCs (for --stats), any window
    ("threatfox_recent", "*"): {
        "query_status": "ok",
        "data": [
            {"id": "1301001", "ioc": "45.155.204.10:443", "ioc_type": "ip:port", "threat_type": "botnet_cc", "malware": "win.cobalt_strike", "malware_printable": "Cobalt Strike", "confidence_level": 80, "first_seen": "2026-07-14 02:11:09 UTC"},
            {"id": "1301002", "ioc": "hxxp-update-cdn.top", "ioc_type": "domain", "threat_type": "botnet_cc", "malware": "win.cobalt_strike", "malware_printable": "Cobalt Strike", "confidence_level": 75, "first_seen": "2026-07-14 09:42:51 UTC"},
            {"id": "1301003", "ioc": "91.92.240.55:8443", "ioc_type": "ip:port", "threat_type": "botnet_cc", "malware": "win.cobalt_strike", "malware_printable": "Cobalt Strike", "confidence_level": 70, "first_seen": "2026-07-15 11:05:33 UTC"},
            {"id": "1301004", "ioc": "193.29.13.201:80", "ioc_type": "ip:port", "threat_type": "botnet_cc", "malware": "win.cobalt_strike", "malware_printable": "Cobalt Strike", "confidence_level": 65, "first_seen": "2026-07-18 22:17:40 UTC"},
            {"id": "1301005", "ioc": "lumma-panel-live.sbs", "ioc_type": "domain", "threat_type": "botnet_cc", "malware": "win.lumma", "malware_printable": "Lumma Stealer", "confidence_level": 85, "first_seen": "2026-07-15 05:28:02 UTC"},
            {"id": "1301006", "ioc": "http://185.196.10.233/build/lm.exe", "ioc_type": "url", "threat_type": "payload_delivery", "malware": "win.lumma", "malware_printable": "Lumma Stealer", "confidence_level": 90, "first_seen": "2026-07-16 13:50:19 UTC"},
            {"id": "1301007", "ioc": "steam-community-verify.win", "ioc_type": "domain", "threat_type": "phishing", "malware": "win.lumma", "malware_printable": "Lumma Stealer", "confidence_level": 75, "first_seen": "2026-07-19 07:33:57 UTC"},
            {"id": "1301008", "ioc": "77.91.68.29:4449", "ioc_type": "ip:port", "threat_type": "botnet_cc", "malware": "win.asyncrat", "malware_printable": "AsyncRAT", "confidence_level": 80, "first_seen": "2026-07-16 18:09:44 UTC"},
            {"id": "1301009", "ioc": "async-dns-sync.duckdns.org", "ioc_type": "domain", "threat_type": "botnet_cc", "malware": "win.asyncrat", "malware_printable": "AsyncRAT", "confidence_level": 70, "first_seen": "2026-07-17 01:56:12 UTC"},
            {"id": "1301010", "ioc": "45.88.90.171:6606", "ioc_type": "ip:port", "threat_type": "botnet_cc", "malware": "win.asyncrat", "malware_printable": "AsyncRAT", "confidence_level": 75, "first_seen": "2026-07-19 15:21:38 UTC"},
            {"id": "1301011", "ioc": "invoice-secure-docs.info", "ioc_type": "domain", "threat_type": "botnet_cc", "malware": "win.emotet", "malware_printable": "Emotet", "confidence_level": 85, "first_seen": "2026-07-17 10:44:29 UTC"},
            {"id": "1301012", "ioc": "http://102.165.30.9/forms/e5.dll", "ioc_type": "url", "threat_type": "payload_delivery", "malware": "win.emotet", "malware_printable": "Emotet", "confidence_level": 80, "first_seen": "2026-07-18 04:12:56 UTC"},
            {"id": "1301013", "ioc": "146.70.149.32:2404", "ioc_type": "ip:port", "threat_type": "botnet_cc", "malware": "win.remcos", "malware_printable": "Remcos RAT", "confidence_level": 70, "first_seen": "2026-07-18 12:38:14 UTC"},
            {"id": "1301014", "ioc": "http://176.65.144.60/bins/tsunami.x86", "ioc_type": "url", "threat_type": "payload_delivery", "malware": "elf.tsunami", "malware_printable": "Tsunami", "confidence_level": 75, "first_seen": "2026-07-19 20:04:47 UTC"},
        ],
    },
}
