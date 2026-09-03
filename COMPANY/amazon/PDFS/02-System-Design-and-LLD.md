# System Design & LLD Pack — Amazon SDE-I (L4)

## What you're actually being asked for

At L4 the design round is called **"Logical and Maintainable Code"** and it is **object-oriented design**, not distributed systems. Candidate reports are consistent: *"If you're L4 loop, then maybe not system but OOP."* You will write **real classes with real methods**. One report is blunt about the format — interviewers want "one step past the UML diagram," and you may only have ~25 minutes of actual design time after the LP questions.

So: **don't spend 20 minutes drawing UML.** Sketch class names fast, get the interviewer's agreement, then code.

That said, a minority of L4 loops do include a light HLD round, and the Bar Raiser may push a design question at you. Section 3 covers that at the depth L4 needs — no more.

**Every problem below follows the format you asked for:**

1. **Clarify** — the questions to ask, and what each one buys you
2. **Final idea** — the design in three sentences
3. **Entities and their functions** — the class list with responsibilities
4. **OOP + design pattern** — which principle each class demonstrates and which pattern fits
5. **Basic code** — compilable Java you could produce in 25 minutes

Java throughout, because the OOP round is *about* types and interfaces and Java makes them visible.

---

# 1. The reference sheet (learn this before the problems)

## 1.1 The four OOP pillars — how to *demonstrate* them, not define them

Reciting definitions scores nothing. Interviewers want to see the pillar *used*. Here is the difference:

| Pillar | Weak answer | What actually earns the point |
|---|---|---|
| **Encapsulation** | "Data hiding with private fields." | Making `ParkingSpot.isOccupied` private with a `park()` method that validates and mutates — so no caller can put the object into an illegal state. |
| **Abstraction** | "Hiding complexity." | Exposing `PricingStrategy.calculate(ticket)` so callers never learn whether it's hourly, flat, or tiered. |
| **Inheritance** | "Child extends parent." | An abstract `Vehicle` with `getSize()`, subclassed by `Car`, `Truck`, `Motorcycle`. **Say why inheritance and not composition** — you inherit only for genuine is-a relationships with shared behavior. |
| **Polymorphism** | "Many forms." | A `List<Vehicle>` where calling `getSize()` dispatches to the right subclass — the parking lot code has zero `instanceof` checks. |

**The sentence that separates candidates:** *"I'm using composition here rather than inheritance, because a ParkingLot **has** floors — it isn't a kind of floor."* Favor composition over inheritance, and be able to say why.

## 1.2 SOLID, compressed to what you'll actually cite

- **S — Single Responsibility.** One reason to change. `PaymentProcessor` handles payment; it does not also print receipts.
- **O — Open/Closed.** Adding a new pricing rule should mean adding a class, not editing a switch statement. This is what motivates Strategy.
- **L — Liskov Substitution.** Any `Vehicle` subclass must work anywhere a `Vehicle` is expected, without surprises.
- **I — Interface Segregation.** Small focused interfaces. Don't force `Motorcycle` to implement `loadCargo()`.
- **D — Dependency Inversion.** Depend on `PricingStrategy` (the interface), not `HourlyPricing` (the concrete class). This is what makes testing possible.

**In the room:** you don't need all five. Name **one or two where they actually apply** and explain the concrete benefit. Reciting all five unprompted reads as memorized.

## 1.3 The five patterns that cover ~90% of LLD rounds

If you learn only four, make them **Strategy, State, Observer, Factory**.

| Pattern | Use when | Recognize it by | Shows up in |
|---|---|---|---|
| **Strategy** | An algorithm needs to be swappable at runtime | An interface with one method, several implementations, injected into a context | Pricing, eviction policy, elevator dispatch, rate-limit algorithm |
| **State** | An object's behavior changes with its mode, and you'd otherwise write a giant if/else | Each state is a class; states decide their own transitions | Vending machine, elevator, order lifecycle, upload lifecycle |
| **Observer** | One change must notify many listeners, decoupled | Subject holds a list of subscribers; `notifyAll()` | Notifications, S3 event notifications, cache invalidation |
| **Factory** | Object creation depends on input and you want it in one place | A `create(type)` method returning the interface | Vehicle creation, storage-class selection, log-handler creation |
| **Singleton** | Exactly one instance must exist | Private constructor, static accessor | Config, connection pool, the lot/system object itself |

**Two honest cautions worth voicing.**
- **Singleton is often a smell.** It's a global variable with better manners, and it makes unit testing hard. Use it, but say: *"I'm using a singleton for the config here, though I'd inject it in production code so it's mockable."* That one sentence signals maturity.
- **Don't pattern-stuff.** Forcing five patterns into a parking lot is a negative signal. Use the ones the problem asks for and say why.

**Others worth naming if they come up:** Builder (many optional constructor params), Decorator (layering behavior — compression on encryption on a stream), Chain of Responsibility (a request passing through handlers — logging, middleware), Adapter (bridging incompatible interfaces), Command (encapsulating a request as an object — undo, queued jobs).

## 1.4 Concurrency vocabulary for the L4 round

Reports show CS-fundamentals questions surface in these rounds — mutex vs semaphore came up specifically. Have these ready:

- **Mutex:** one holder at a time; only the holder may release it. Protects a critical section.
- **Semaphore:** a counter permitting N concurrent holders; any thread may release. Models a resource pool (say, N parking spots).
- **`synchronized` vs `ReentrantLock` (Java):** the latter adds `tryLock`, timeouts, interruptibility, and fairness options.
- **`ConcurrentHashMap`:** lock-striped, so concurrent readers and writers on different keys don't block each other. Reach for this before `Collections.synchronizedMap`.
- **Atomics (`AtomicInteger`):** compare-and-swap, lock-free, right for counters.
- **Deadlock's four conditions:** mutual exclusion, hold-and-wait, no preemption, circular wait. Break any one — the usual fix is a **global lock ordering** to kill circular wait.

**When an interviewer says "make it thread-safe," the correct first answer is the simple one:** one lock around the mutating operations. *Then* discuss contention and finer-grained alternatives. Jumping straight to lock-free reads as showing off.

---

# 2. Low-Level Design Problems

## 2.1 Design a Parking Lot

The single most-reported Amazon LLD question. One 2025 SDE-1 report describes it as "Parking Lot with many constraints" in a 30-minute slot. Know it cold — the goal is to spend your thinking time on their specific constraints, not on the base structure.

### 1 — Clarify

Ask these, then stop. Two minutes, maximum four questions.

| Question | Why it matters |
|---|---|
| "Multiple floors, or one level?" | Decides whether `Floor` exists as a class at all |
| "What vehicle types, and do spot sizes differ?" | Drives the `Vehicle`/`SpotType` hierarchy — this is the core modeling decision |
| "Is pricing flat or time-based? Different rates per vehicle type?" | Justifies the Strategy pattern |
| "Do I need payment, or is issuing and closing a ticket enough?" | Scopes the problem so you finish |
| "Multiple entrances operating concurrently?" | Signals whether thread-safety is in scope |

**Then state your scope out loud:** *"I'll build multi-floor with three vehicle sizes, ticket issue and close, and a pluggable pricing strategy. I'll leave payment gateway integration behind an interface. Sound right?"* Getting that nod before coding is the single highest-value thirty seconds of the round.

### 2 — Final idea

A `ParkingLot` owns `Floor`s; each `Floor` owns `ParkingSpot`s bucketed by size. Parking = find the smallest compatible free spot, occupy it, issue a `Ticket` with an entry timestamp. Unparking = look up the ticket, free the spot, and hand the ticket to a `PricingStrategy` to compute the fee. All spot lookup and pricing hide behind interfaces so new vehicle types or rate cards are new classes, not edits to existing ones.

### 3 — Entities and their functions

| Entity | Responsibility | Key methods |
|---|---|---|
| `Vehicle` (abstract) | Holds a plate and knows the spot size it needs | `getSize()`, `getLicensePlate()` |
| `Car`, `Motorcycle`, `Truck` | Concrete sizes | inherit |
| `SpotSize` (enum) | SMALL / MEDIUM / LARGE; ordered so smaller fits larger | — |
| `ParkingSpot` | Owns its own occupancy; never lets an outsider corrupt it | `assign(v)`, `release()`, `isFree()` |
| `Floor` | Finds a free spot on this level | `findFreeSpot(size)`, `availableCount()` |
| `Ticket` | Immutable record: id, plate, spot, entry time | `getEntryTime()`, `getSpot()` |
| `PricingStrategy` (interface) | Computes fee from a ticket and exit time | `calculate(ticket, exitTime)` |
| `HourlyPricing`, `FlatRatePricing` | Concrete rate cards | implements |
| `ParkingLot` | Orchestrates park/unpark, holds active tickets | `park(v)`, `unpark(ticketId)` |
| `VehicleFactory` | Creates the right `Vehicle` from a type string | `create(type, plate)` |

### 4 — OOP + design pattern

**OOP demonstrated.**
- *Encapsulation:* `ParkingSpot.occupant` is private. Only `assign()`/`release()` mutate it, and `assign()` throws if already taken — the object cannot enter an illegal state.
- *Inheritance:* `Vehicle` → `Car`/`Truck`/`Motorcycle`, a genuine is-a relationship with shared identity behavior.
- *Polymorphism:* `spot.canFit(vehicle)` calls `vehicle.getSize()` with no `instanceof` anywhere. Adding `ElectricCar` requires zero changes to `ParkingLot`.
- *Abstraction:* callers say `lot.park(vehicle)` and never learn about floors or search order.
- *Composition over inheritance:* a lot **has** floors; a floor **has** spots. Say this explicitly.

**Patterns.**
- **Strategy** for `PricingStrategy` — the headline pattern here. A new weekend rate is a new class, satisfying Open/Closed.
- **Factory** for `VehicleFactory` — creation logic in one place.
- **Singleton** for `ParkingLot` if there's exactly one — but voice the testability caveat.
- **Observer** if they add "notify a display board when a floor fills." Mention it only if asked.

### 5 — Basic code

```java
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

enum SpotSize { SMALL, MEDIUM, LARGE }

abstract class Vehicle {
    private final String licensePlate;
    protected Vehicle(String licensePlate) { this.licensePlate = licensePlate; }
    public String getLicensePlate() { return licensePlate; }
    public abstract SpotSize getSize();
}

class Motorcycle extends Vehicle {
    public Motorcycle(String p) { super(p); }
    public SpotSize getSize() { return SpotSize.SMALL; }
}
class Car extends Vehicle {
    public Car(String p) { super(p); }
    public SpotSize getSize() { return SpotSize.MEDIUM; }
}
class Truck extends Vehicle {
    public Truck(String p) { super(p); }
    public SpotSize getSize() { return SpotSize.LARGE; }
}

class VehicleFactory {                                  // Factory
    public static Vehicle create(String type, String plate) {
        switch (type.toUpperCase()) {
            case "MOTORCYCLE": return new Motorcycle(plate);
            case "CAR":        return new Car(plate);
            case "TRUCK":      return new Truck(plate);
            default: throw new IllegalArgumentException("Unknown type: " + type);
        }
    }
}

class ParkingSpot {
    private final String id;
    private final SpotSize size;
    private Vehicle occupant;                           // encapsulated state

    public ParkingSpot(String id, SpotSize size) { this.id = id; this.size = size; }

    public String getId()      { return id; }
    public SpotSize getSize()  { return size; }
    public boolean isFree()    { return occupant == null; }

    /** A vehicle fits if the spot is at least as large as the vehicle needs. */
    public boolean canFit(Vehicle v) {
        return isFree() && size.ordinal() >= v.getSize().ordinal();
    }

    public synchronized void assign(Vehicle v) {
        if (!canFit(v)) throw new IllegalStateException("Spot " + id + " unavailable");
        this.occupant = v;
    }

    public synchronized void release() { this.occupant = null; }
}

class Floor {
    private final int number;
    private final List<ParkingSpot> spots = new ArrayList<>();

    public Floor(int number) { this.number = number; }
    public int getNumber() { return number; }
    public void addSpot(ParkingSpot s) { spots.add(s); }

    /** Smallest spot that fits — avoids wasting a truck bay on a motorcycle. */
    public Optional<ParkingSpot> findFreeSpot(Vehicle v) {
        return spots.stream()
                    .filter(s -> s.canFit(v))
                    .min(Comparator.comparingInt(s -> s.getSize().ordinal()));
    }

    public long availableCount() { return spots.stream().filter(ParkingSpot::isFree).count(); }
}

class Ticket {
    private final String id;
    private final String licensePlate;
    private final ParkingSpot spot;
    private final Instant entryTime;

    public Ticket(String id, String plate, ParkingSpot spot) {
        this.id = id; this.licensePlate = plate;
        this.spot = spot; this.entryTime = Instant.now();
    }
    public String getId()          { return id; }
    public ParkingSpot getSpot()   { return spot; }
    public Instant getEntryTime()  { return entryTime; }
    public String getLicensePlate(){ return licensePlate; }
}

interface PricingStrategy {                             // Strategy
    double calculate(Ticket ticket, Instant exitTime);
}

class HourlyPricing implements PricingStrategy {
    private final double ratePerHour;
    public HourlyPricing(double ratePerHour) { this.ratePerHour = ratePerHour; }
    public double calculate(Ticket t, Instant exit) {
        long hours = Math.max(1, Duration.between(t.getEntryTime(), exit).toHours());
        return hours * ratePerHour;                     // minimum one hour
    }
}

class FlatRatePricing implements PricingStrategy {
    private final double flat;
    public FlatRatePricing(double flat) { this.flat = flat; }
    public double calculate(Ticket t, Instant exit) { return flat; }
}

class ParkingLot {
    private final List<Floor> floors = new ArrayList<>();
    private final Map<String, Ticket> activeTickets = new ConcurrentHashMap<>();
    private PricingStrategy pricing;                    // injected, not hardcoded

    public ParkingLot(PricingStrategy pricing) { this.pricing = pricing; }

    public void addFloor(Floor f) { floors.add(f); }
    public void setPricing(PricingStrategy p) { this.pricing = p; }   // swap at runtime

    public synchronized Ticket park(Vehicle vehicle) {
        for (Floor floor : floors) {
            Optional<ParkingSpot> found = floor.findFreeSpot(vehicle);
            if (found.isPresent()) {
                ParkingSpot spot = found.get();
                spot.assign(vehicle);
                Ticket ticket = new Ticket(UUID.randomUUID().toString(),
                                           vehicle.getLicensePlate(), spot);
                activeTickets.put(ticket.getId(), ticket);
                return ticket;
            }
        }
        throw new IllegalStateException("Parking lot full for size " + vehicle.getSize());
    }

    public synchronized double unpark(String ticketId) {
        Ticket ticket = activeTickets.remove(ticketId);
        if (ticket == null) throw new IllegalArgumentException("Invalid ticket: " + ticketId);
        ticket.getSpot().release();
        return pricing.calculate(ticket, Instant.now());
    }
}
```

**Complexity.** `park` is O(F · S) with a linear scan. **Volunteer the fix:** keep a `Map<SpotSize, PriorityQueue<ParkingSpot>>` of free spots per floor, making both park and unpark O(log S). Say this even if you don't code it — it's the optimization they're waiting for.

**Follow-ups to expect.**
- *"Two cars arrive at the last spot simultaneously."* → `synchronized` on `park` serializes it; the loser gets the exception. For scale, lock per floor rather than per lot to reduce contention.
- *"Reserved / handicapped spots."* → Add a `SpotFeature` set to `ParkingSpot` and a matching requirement on `Vehicle`; extend `canFit`. Don't add a subclass — that's inheritance where composition belongs.
- *"Find my car by plate."* → A `Map<String, Ticket>` secondary index. Note the memory cost.

---

## 2.2 Design an Object Store (S3-like Key-Value Store)

**Why this one is in the pack.** It's the LLD most likely to be handed to you *by an S3 interviewer specifically*, because it's their domain. It also lets you show off versioning, lifecycle rules, and prefix listing — the things that make S3 S3. Treat this as the highest-ROI problem in this file if you're interviewing with storage.

### 1 — Clarify

| Question | Why it matters |
|---|---|
| "Single-node in-memory, or am I designing the distributed system?" | For L4 this is almost always the in-memory component design. Confirm it and scope down. |
| "Do I need versioning — multiple versions of the same key?" | This is the interesting half of the problem. If yes, your value type becomes a list. |
| "Flat keys with a delimiter, or real nested directories?" | Real S3 keys are **flat strings**; hierarchy is faked by `ListObjectsV2` with a prefix and delimiter. Knowing this is a strong signal — ask the question in a way that shows you know. |
| "Lifecycle rules — expire or transition objects by age?" | Justifies the Strategy pattern for storage classes. |
| "Metadata and content type, or just bytes?" | Small scope decision, quick to ask. |

**Scope statement:** *"I'll build an in-memory store with buckets, versioned objects, prefix listing with a delimiter, and pluggable storage classes. I'll keep durability and replication out of scope since this is the component-level design."*

### 2 — Final idea

An `ObjectStore` holds named `Bucket`s. Each `Bucket` maps a flat key to a `VersionedObject`, which is an append-only list of immutable `S3Object` versions plus delete markers. Reads default to the newest version but accept a version id. Listing walks a sorted key structure from the prefix, truncating at the delimiter to synthesize "common prefixes." Storage class and lifecycle behavior sit behind interfaces so cold-tiering is an added class, not an edit.

### 3 — Entities and their functions

| Entity | Responsibility | Key methods |
|---|---|---|
| `ObjectStore` | Top-level bucket registry | `createBucket`, `deleteBucket`, `getBucket` |
| `Bucket` | Owns a key namespace; enforces versioning policy | `put`, `get`, `delete`, `list` |
| `S3Object` | **Immutable** — data, metadata, version id, timestamp, storage class | getters only |
| `VersionedObject` | Ordered version chain for one key | `addVersion`, `latest`, `getVersion` |
| `DeleteMarker` | A tombstone version — makes `get` return not-found without erasing history | — |
| `StorageClass` (interface) | Cost and retrieval behavior per tier | `retrievalLatencyMs()`, `costPerGbMonth()` |
| `StandardStorage`, `GlacierStorage` | Concrete tiers | implements |
| `LifecycleRule` | Predicate plus action for aging objects | `applies(obj)`, `apply(obj)` |
| `ListResult` | Keys plus common prefixes plus a continuation token | — |
| `EventPublisher` | Notifies subscribers on put/delete | `subscribe`, `publish` |

### 4 — OOP + design pattern

**OOP demonstrated.**
- *Immutability + encapsulation:* `S3Object` is final with final fields and defensive copies of the byte array. This is the honest modeling choice — S3 objects genuinely are immutable, and overwriting creates a *new version*. Saying that shows domain understanding.
- *Abstraction:* the caller says `bucket.get(key)` and never learns whether that's a hot in-memory hit or a cold-tier fetch.
- *Polymorphism:* `StorageClass` implementations are interchangeable.
- *Composition:* `ObjectStore` **has** buckets; `Bucket` **has** versioned objects. No inheritance chain, because none of these is-a the other.

**Patterns.**
- **Strategy** for `StorageClass` and for `LifecycleRule` actions.
- **Observer** for `EventPublisher` — this is literally S3 Event Notifications, so naming it is a domain point as well as a pattern point.
- **Factory** for constructing the right `StorageClass` from a tier name.
- **Builder** for `S3Object` if metadata grows optional fields.

### 5 — Basic code

```java
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

interface StorageClass {
    String name();
    long retrievalLatencyMs();
    double costPerGbMonth();
}

class StandardStorage implements StorageClass {
    public String name() { return "STANDARD"; }
    public long retrievalLatencyMs() { return 10; }
    public double costPerGbMonth() { return 0.023; }
}

class GlacierStorage implements StorageClass {
    public String name() { return "GLACIER"; }
    public long retrievalLatencyMs() { return 4L * 60 * 60 * 1000; }   // hours
    public double costPerGbMonth() { return 0.004; }
}

/** Immutable. Overwriting a key creates a new S3Object, never mutates one. */
final class S3Object {
    private final String key;
    private final byte[] data;
    private final String versionId;
    private final Instant lastModified;
    private final Map<String, String> metadata;
    private final StorageClass storageClass;
    private final boolean deleteMarker;

    private S3Object(String key, byte[] data, String versionId,
                     Map<String, String> metadata, StorageClass sc, boolean deleteMarker) {
        this.key = key;
        this.data = data == null ? null : data.clone();          // defensive copy
        this.versionId = versionId;
        this.lastModified = Instant.now();
        this.metadata = Map.copyOf(metadata == null ? Map.of() : metadata);
        this.storageClass = sc;
        this.deleteMarker = deleteMarker;
    }

    static S3Object of(String key, byte[] data, Map<String, String> md, StorageClass sc) {
        return new S3Object(key, data, UUID.randomUUID().toString(), md, sc, false);
    }

    static S3Object tombstone(String key) {
        return new S3Object(key, null, UUID.randomUUID().toString(),
                            Map.of(), new StandardStorage(), true);
    }

    public String getKey()            { return key; }
    public byte[] getData()           { return data == null ? null : data.clone(); }
    public String getVersionId()      { return versionId; }
    public Instant getLastModified()  { return lastModified; }
    public boolean isDeleteMarker()   { return deleteMarker; }
    public StorageClass getStorageClass() { return storageClass; }
    public long size()                { return data == null ? 0 : data.length; }
}

/** Newest version last. Delete markers live in the chain like any other version. */
class VersionedObject {
    private final List<S3Object> versions = new ArrayList<>();

    synchronized void addVersion(S3Object obj) { versions.add(obj); }

    synchronized Optional<S3Object> latest() {
        if (versions.isEmpty()) return Optional.empty();
        S3Object head = versions.get(versions.size() - 1);
        return head.isDeleteMarker() ? Optional.empty() : Optional.of(head);
    }

    synchronized Optional<S3Object> getVersion(String versionId) {
        return versions.stream().filter(v -> v.getVersionId().equals(versionId)).findFirst();
    }

    synchronized List<S3Object> allVersions() { return List.copyOf(versions); }
}

class ListResult {
    final List<String> keys;
    final List<String> commonPrefixes;
    final String nextToken;
    ListResult(List<String> keys, List<String> commonPrefixes, String nextToken) {
        this.keys = keys; this.commonPrefixes = commonPrefixes; this.nextToken = nextToken;
    }
}

interface StoreListener { void onEvent(String type, String bucket, String key); }

class EventPublisher {                                        // Observer
    private final List<StoreListener> listeners = new ArrayList<>();
    void subscribe(StoreListener l) { listeners.add(l); }
    void publish(String type, String bucket, String key) {
        for (StoreListener l : listeners) l.onEvent(type, bucket, key);
    }
}

class Bucket {
    private final String name;
    private final boolean versioningEnabled;
    // TreeMap keeps keys sorted -> prefix listing is a range scan, not a full scan.
    private final NavigableMap<String, VersionedObject> objects = new TreeMap<>();
    private final EventPublisher events;

    Bucket(String name, boolean versioningEnabled, EventPublisher events) {
        this.name = name; this.versioningEnabled = versioningEnabled; this.events = events;
    }

    public synchronized S3Object put(String key, byte[] data,
                                     Map<String, String> md, StorageClass sc) {
        S3Object obj = S3Object.of(key, data, md, sc);
        VersionedObject vo = objects.computeIfAbsent(key, k -> new VersionedObject());
        if (!versioningEnabled) objects.put(key, vo = new VersionedObject());  // overwrite
        vo.addVersion(obj);
        events.publish("ObjectCreated:Put", name, key);
        return obj;
    }

    public synchronized Optional<S3Object> get(String key) {
        VersionedObject vo = objects.get(key);
        return vo == null ? Optional.empty() : vo.latest();
    }

    public synchronized Optional<S3Object> get(String key, String versionId) {
        VersionedObject vo = objects.get(key);
        return vo == null ? Optional.empty() : vo.getVersion(versionId);
    }

    public synchronized void delete(String key) {
        VersionedObject vo = objects.get(key);
        if (vo == null) return;
        if (versioningEnabled) {
            vo.addVersion(S3Object.tombstone(key));   // history preserved
        } else {
            objects.remove(key);
        }
        events.publish("ObjectRemoved:Delete", name, key);
    }

    /**
     * ListObjectsV2 semantics. With a delimiter, keys sharing a segment collapse
     * into a single "common prefix" -- this is how S3 fakes folders over flat keys.
     */
    public synchronized ListResult list(String prefix, String delimiter,
                                        String startAfter, int maxKeys) {
        List<String> keys = new ArrayList<>();
        Set<String> prefixes = new TreeSet<>();
        String from = (startAfter != null && !startAfter.isEmpty()) ? startAfter : prefix;
        String nextToken = null;

        for (Map.Entry<String, VersionedObject> e : objects.tailMap(from, false).entrySet()) {
            String key = e.getKey();
            if (!key.startsWith(prefix)) break;                 // sorted -> safe to stop
            if (e.getValue().latest().isEmpty()) continue;      // tombstoned

            if (delimiter != null && !delimiter.isEmpty()) {
                int idx = key.indexOf(delimiter, prefix.length());
                if (idx >= 0) {
                    prefixes.add(key.substring(0, idx + delimiter.length()));
                    continue;
                }
            }
            keys.add(key);
            if (keys.size() + prefixes.size() >= maxKeys) { nextToken = key; break; }
        }
        return new ListResult(keys, new ArrayList<>(prefixes), nextToken);
    }
}

class ObjectStore {
    private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();
    private final EventPublisher events = new EventPublisher();

    public Bucket createBucket(String name, boolean versioning) {
        return buckets.computeIfAbsent(name, n -> new Bucket(n, versioning, events));
    }
    public Optional<Bucket> getBucket(String name) {
        return Optional.ofNullable(buckets.get(name));
    }
    public void subscribe(StoreListener l) { events.subscribe(l); }
}
```

**Complexity.** `put`/`get` are **O(log n)** on the TreeMap (swap for a HashMap if you drop listing — say so). `list` is **O(log n + k)** where k is the keys scanned — the sorted map is what makes prefix listing a range scan rather than a full scan. Call that out; it's the design decision that matters.

**Follow-ups to have ready.**
- *"Now make it durable."* → Write-ahead log for the metadata, content-addressed chunks for the data, erasure coding across failure domains. Note S3's advertised eleven-nines durability comes from redundancy across multiple availability zones, not from any single copy.
- *"Multipart upload."* → An `UploadSession` holding part number → chunk, with a `complete()` that validates all parts are present and concatenates. Part boundaries are an **interval problem** — connect it to Merge Intervals.
- *"Range GET."* → `get(key, byteStart, byteEnd)`; slice the buffer. In a real system this maps to chunk lookup, another interval problem.
- *"Lifecycle: move to Glacier after 30 days."* → `LifecycleRule` with a predicate on `lastModified` and an action that rewrites `storageClass`. A background sweeper applies rules. This is where Strategy pays off.

---

## 2.3 Design an LRU Cache (as an OOD round, not a LeetCode round)

The difference from the coding version: here they want **extensibility and thread-safety**, not just O(1). Eviction policy should be swappable.

### 1 — Clarify

- "Fixed entry count, or a byte-size budget?" (Byte budget is more realistic and more interesting.)
- "Is TTL expiry in scope?"
- "Single-threaded, or concurrent readers and writers?"
- "Should the eviction policy be pluggable — LRU today, LFU later?"
- "What happens on a miss — return null, or load through from a backing store?"

### 2 — Final idea

A `Cache<K,V>` interface with a `LinkedHashMapCache` or hand-rolled implementation. Eviction is delegated to an `EvictionPolicy<K>` that observes accesses and nominates a victim — so LRU, LFU, and FIFO are three classes behind one interface. A `ReadWriteLock` (or per-shard locks) provides thread safety. An optional `CacheLoader` turns a miss into a load-through.

### 3 — Entities and their functions

| Entity | Responsibility | Key methods |
|---|---|---|
| `Cache<K,V>` (interface) | The public contract | `get`, `put`, `remove`, `size` |
| `InMemoryCache<K,V>` | HashMap plus policy, enforces capacity | implements above |
| `EvictionPolicy<K>` (interface) | Tracks usage, nominates a victim | `recordAccess(k)`, `recordInsert(k)`, `evictKey()`, `remove(k)` |
| `LruPolicy<K>` | Doubly linked list ordered by recency | implements |
| `LfuPolicy<K>` | Frequency buckets | implements |
| `CacheEntry<V>` | Value, size in bytes, expiry timestamp | `isExpired()` |
| `CacheLoader<K,V>` (interface) | Load-through on miss | `load(k)` |
| `CacheStats` | Hits, misses, evictions | `hitRate()` |

### 4 — OOP + design pattern

- **Strategy** for `EvictionPolicy` — the headline. Swapping LRU for LFU touches zero lines of `InMemoryCache`. That's Open/Closed and Dependency Inversion in one move.
- **Observer**, informally: the cache notifies the policy of every access, so the policy maintains its own ordering without the cache knowing how.
- **Decorator** if they add "now make it a write-through cache" — wrap the base cache rather than editing it.
- *Encapsulation:* the linked list lives entirely inside `LruPolicy`; nothing outside can corrupt the ordering.
- *Generics:* type-safe over any `K`/`V` — worth pointing out as an alternative to inheritance for reuse.

### 5 — Basic code

```java
import java.util.*;
import java.util.concurrent.locks.ReentrantReadWriteLock;

interface EvictionPolicy<K> {
    void recordAccess(K key);
    void recordInsert(K key);
    void remove(K key);
    K evictKey();                 // null if nothing to evict
}

class LruPolicy<K> implements EvictionPolicy<K> {
    // accessOrder=true makes LinkedHashMap reorder on every get -> recency order for free.
    private final LinkedHashMap<K, Boolean> order = new LinkedHashMap<>(16, 0.75f, true);

    public void recordAccess(K key) { order.get(key); }
    public void recordInsert(K key) { order.put(key, Boolean.TRUE); }
    public void remove(K key)       { order.remove(key); }

    public K evictKey() {
        Iterator<K> it = order.keySet().iterator();
        if (!it.hasNext()) return null;
        K victim = it.next();                       // eldest = least recently used
        it.remove();
        return victim;
    }
}

class LfuPolicy<K> implements EvictionPolicy<K> {
    private final Map<K, Integer> freq = new HashMap<>();
    private final TreeMap<Integer, LinkedHashSet<K>> buckets = new TreeMap<>();

    public void recordInsert(K key) { freq.put(key, 1); bucket(1).add(key); }

    public void recordAccess(K key) {
        Integer f = freq.get(key);
        if (f == null) return;
        buckets.get(f).remove(key);
        if (buckets.get(f).isEmpty()) buckets.remove(f);
        freq.put(key, f + 1);
        bucket(f + 1).add(key);
    }

    public void remove(K key) {
        Integer f = freq.remove(key);
        if (f == null) return;
        buckets.get(f).remove(key);
        if (buckets.get(f).isEmpty()) buckets.remove(f);
    }

    public K evictKey() {
        if (buckets.isEmpty()) return null;
        Map.Entry<Integer, LinkedHashSet<K>> lowest = buckets.firstEntry();
        Iterator<K> it = lowest.getValue().iterator();
        K victim = it.next();                       // LRU within the lowest frequency
        it.remove();
        if (lowest.getValue().isEmpty()) buckets.remove(lowest.getKey());
        freq.remove(victim);
        return victim;
    }

    private LinkedHashSet<K> bucket(int f) {
        return buckets.computeIfAbsent(f, k -> new LinkedHashSet<>());
    }
}

class CacheEntry<V> {
    final V value;
    final long expiresAtMillis;                     // Long.MAX_VALUE = never
    CacheEntry(V value, long ttlMillis) {
        this.value = value;
        this.expiresAtMillis = ttlMillis <= 0
            ? Long.MAX_VALUE : System.currentTimeMillis() + ttlMillis;
    }
    boolean isExpired() { return System.currentTimeMillis() > expiresAtMillis; }
}

interface Cache<K, V> {
    Optional<V> get(K key);
    void put(K key, V value);
    void remove(K key);
    int size();
}

class InMemoryCache<K, V> implements Cache<K, V> {
    private final int capacity;
    private final long defaultTtlMillis;
    private final Map<K, CacheEntry<V>> store = new HashMap<>();
    private final EvictionPolicy<K> policy;                    // injected Strategy
    private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock();
    private long hits, misses, evictions;

    public InMemoryCache(int capacity, EvictionPolicy<K> policy, long defaultTtlMillis) {
        this.capacity = capacity;
        this.policy = policy;
        this.defaultTtlMillis = defaultTtlMillis;
    }

    public Optional<V> get(K key) {
        lock.writeLock().lock();          // write lock: a read mutates recency order
        try {
            CacheEntry<V> e = store.get(key);
            if (e == null) { misses++; return Optional.empty(); }
            if (e.isExpired()) {          // lazy expiry
                store.remove(key); policy.remove(key); misses++;
                return Optional.empty();
            }
            policy.recordAccess(key);
            hits++;
            return Optional.of(e.value);
        } finally { lock.writeLock().unlock(); }
    }

    public void put(K key, V value) {
        lock.writeLock().lock();
        try {
            if (store.containsKey(key)) {
                store.put(key, new CacheEntry<>(value, defaultTtlMillis));
                policy.recordAccess(key);
                return;
            }
            if (store.size() >= capacity) {
                K victim = policy.evictKey();
                if (victim != null) { store.remove(victim); evictions++; }
            }
            store.put(key, new CacheEntry<>(value, defaultTtlMillis));
            policy.recordInsert(key);
        } finally { lock.writeLock().unlock(); }
    }

    public void remove(K key) {
        lock.writeLock().lock();
        try { store.remove(key); policy.remove(key); }
        finally { lock.writeLock().unlock(); }
    }

    public int size() {
        lock.readLock().lock();
        try { return store.size(); } finally { lock.readLock().unlock(); }
    }

    public double hitRate() { return hits + misses == 0 ? 0.0 : (double) hits / (hits + misses); }
}
```

**Point to make unprompted:** `get` takes the **write** lock, because reading mutates recency order. Candidates who use a read lock there have a silent race. Noticing it out loud is worth real credit.

**Follow-ups.**
- *"Lock contention is killing us."* → Shard into N segments by `key.hashCode() % N`, each with its own lock and its own policy instance. This is how `ConcurrentHashMap` works and how production caches scale.
- *"Evict by memory, not count."* → Add a `sizeOf(V)` function, track total bytes, and evict in a loop until under budget.
- *"Distributed cache."* → Consistent hashing across nodes so adding a node moves only ~1/N of keys. See §3.5.

---

## 2.4 Design a Rate Limiter

Very likely from a service team — S3 throttles per bucket and per prefix, so this is domain-adjacent.

### 1 — Clarify

- "Per user, per API key, per IP, or global?" (Decides the key of your map.)
- "Which algorithm — fixed window, sliding window, token bucket? Or should I pick and justify?"
- "Should bursts be allowed, or is a strict rate required?" (This alone decides token bucket vs sliding window.)
- "Single process, or distributed across hosts?" (For L4, single process is usually the ask; mention Redis for the distributed case.)
- "On limit: reject with 429, or queue and delay?"

### 2 — Final idea

A `RateLimiter` interface with one method, `allowRequest(clientId)`. Three implementations behind it: fixed window (cheapest, has a boundary-burst flaw), sliding window log (exact, more memory), token bucket (allows controlled bursts, and is what most real APIs use). Per-client state lives in a `ConcurrentHashMap`, and a background sweeper evicts idle clients so memory doesn't grow forever.

### 3 — Entities and their functions

| Entity | Responsibility | Key methods |
|---|---|---|
| `RateLimiter` (interface) | The contract | `allowRequest(clientId)` |
| `FixedWindowLimiter` | Counter per client per window | implements |
| `SlidingWindowLogLimiter` | Deque of timestamps per client | implements |
| `TokenBucketLimiter` | Tokens refilled at a fixed rate | implements |
| `TokenBucket` | Per-client token state, lazily refilled | `tryConsume()` |
| `RateLimitConfig` | Capacity, window, refill rate | getters |
| `RateLimiterFactory` | Builds the right limiter from config | `create(type, config)` |

### 4 — OOP + design pattern

- **Strategy** — the whole point. `allowRequest` is one method; three algorithms implement it; the gateway holds the interface. Adding leaky-bucket later is a new class.
- **Factory** for `RateLimiterFactory`.
- **Singleton** for the shared limiter instance, with the usual testability caveat.
- *Encapsulation:* `TokenBucket` refills itself lazily inside `tryConsume`. No caller ever calls `refill()` — there is no background timer thread and no way to misuse it. Explain the lazy-refill trick; it's the elegant part.

### 5 — Basic code

```java
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

interface RateLimiter { boolean allowRequest(String clientId); }

/** Token bucket: capacity tokens, refilled at refillPerSecond. Allows bursts up to capacity. */
class TokenBucketLimiter implements RateLimiter {
    private final long capacity;
    private final double refillPerSecond;
    private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();

    TokenBucketLimiter(long capacity, double refillPerSecond) {
        this.capacity = capacity; this.refillPerSecond = refillPerSecond;
    }

    public boolean allowRequest(String clientId) {
        return buckets.computeIfAbsent(clientId, id -> new Bucket()).tryConsume();
    }

    private class Bucket {
        private double tokens = capacity;
        private long lastRefillNanos = System.nanoTime();

        synchronized boolean tryConsume() {
            refill();                                  // lazy: no timer thread needed
            if (tokens >= 1) { tokens -= 1; return true; }
            return false;
        }

        private void refill() {
            long now = System.nanoTime();
            double elapsedSeconds = (now - lastRefillNanos) / 1_000_000_000.0;
            tokens = Math.min(capacity, tokens + elapsedSeconds * refillPerSecond);
            lastRefillNanos = now;
        }
    }
}

/** Sliding window log: exact, but stores one timestamp per request in the window. */
class SlidingWindowLogLimiter implements RateLimiter {
    private final int maxRequests;
    private final long windowMillis;
    private final Map<String, Deque<Long>> log = new ConcurrentHashMap<>();

    SlidingWindowLogLimiter(int maxRequests, long windowMillis) {
        this.maxRequests = maxRequests; this.windowMillis = windowMillis;
    }

    public boolean allowRequest(String clientId) {
        Deque<Long> times = log.computeIfAbsent(clientId, k -> new ArrayDeque<>());
        long now = System.currentTimeMillis();
        synchronized (times) {
            while (!times.isEmpty() && times.peekFirst() <= now - windowMillis) {
                times.pollFirst();                     // drop entries that aged out
            }
            if (times.size() < maxRequests) { times.addLast(now); return true; }
            return false;
        }
    }
}

/** Fixed window: cheapest, but allows up to 2x the limit across a window boundary. */
class FixedWindowLimiter implements RateLimiter {
    private final int maxRequests;
    private final long windowMillis;
    private final Map<String, Window> windows = new ConcurrentHashMap<>();

    FixedWindowLimiter(int maxRequests, long windowMillis) {
        this.maxRequests = maxRequests; this.windowMillis = windowMillis;
    }

    public boolean allowRequest(String clientId) {
        Window w = windows.computeIfAbsent(clientId, k -> new Window());
        synchronized (w) {
            long currentWindow = System.currentTimeMillis() / windowMillis;
            if (w.windowId != currentWindow) { w.windowId = currentWindow; w.count = 0; }
            if (w.count < maxRequests) { w.count++; return true; }
            return false;
        }
    }
    private static class Window { long windowId = -1; int count = 0; }
}

class RateLimiterFactory {
    static RateLimiter create(String type, int limit, long windowMillis) {
        switch (type) {
            case "TOKEN_BUCKET":  return new TokenBucketLimiter(limit, limit / (windowMillis / 1000.0));
            case "SLIDING_LOG":   return new SlidingWindowLogLimiter(limit, windowMillis);
            case "FIXED_WINDOW":  return new FixedWindowLimiter(limit, windowMillis);
            default: throw new IllegalArgumentException(type);
        }
    }
}
```

**The trade-off table to say out loud — this is what they're grading:**

| Algorithm | Memory per client | Burst behavior | Flaw |
|---|---|---|---|
| Fixed window | O(1) | Allows a full limit at the end of one window plus a full limit at the start of the next | Up to 2× the limit across a boundary |
| Sliding log | O(requests in window) | Exact | Memory scales with traffic — a burst is expensive |
| Sliding window counter | O(1) | Approximate, weighted blend of two windows | Slight inaccuracy, but usually the right production choice |
| Token bucket | O(1) | Bursts up to capacity, then steady rate | Needs tuning of capacity vs refill |

**Follow-ups.**
- *"Distributed across 100 hosts."* → Centralize counters in Redis with an atomic `INCR` plus `EXPIRE`, or a Lua script for the token bucket to make check-and-consume atomic. Accept slight over-admission, or use per-host quotas of `limit/N` with periodic rebalancing.
- *"Return how long to wait."* → Change the return to a result object carrying `retryAfterMillis`, computed from the refill rate. Real APIs send this as a `Retry-After` header.

---

## 2.5 Design an Elevator System

Reported repeatedly for Amazon SDE-1. The interviewer is watching for the **state machine** and a **pluggable dispatch strategy**, because the follow-up is always "now add more elevators."

### 1 — Clarify

- "How many elevators, how many floors?"
- "Two request types — a hall call from a floor with a direction, and a cabin request from inside for a specific floor. Should I model both?" (Yes, and asking shows you've thought about it.)
- "What scheduling — nearest car, or true SCAN where an elevator finishes its current direction first?"
- "Weight limits, express floors, out-of-service state?"
- "Do I simulate time steps, or just model the state and decisions?"

### 2 — Final idea

Each `Elevator` is a state machine — IDLE, MOVING_UP, MOVING_DOWN, DOORS_OPEN, MAINTENANCE — holding sorted sets of target floors. An `ElevatorController` receives requests and hands them to a `DispatchStrategy` that scores every elevator and picks a winner. Each tick, every elevator advances one floor toward its next target and services stops. Swapping dispatch algorithms means swapping one injected object.

### 3 — Entities and their functions

| Entity | Responsibility | Key methods |
|---|---|---|
| `Direction` (enum) | UP / DOWN / IDLE | — |
| `ElevatorState` (enum or classes) | IDLE, MOVING_UP, MOVING_DOWN, DOORS_OPEN, MAINTENANCE | — |
| `Request` | Origin floor, destination, direction, internal or external | getters |
| `Elevator` | Owns its position, direction, and target sets; steps itself | `addTarget`, `step()`, `canServe(req)` |
| `DispatchStrategy` (interface) | Chooses which elevator takes a request | `selectElevator(list, req)` |
| `NearestCarStrategy`, `ScanStrategy` | Concrete algorithms | implements |
| `ElevatorController` | Accepts requests, delegates dispatch, drives ticks | `requestElevator`, `tick()` |
| `Display` | Observes elevators and shows position | `update(elevator)` |

### 4 — OOP + design pattern

- **State** — each elevator mode determines its own legal transitions. This is what stops the giant if/else that this problem invites. Even as an enum with a `next()` method, name the pattern.
- **Strategy** for `DispatchStrategy` — the follow-up ("optimize for energy," "now use SCAN") becomes a new class instead of a rewrite. This is the pattern that earns the round.
- **Observer** for `Display` and for floor indicators.
- **Singleton** for `ElevatorController`.
- *Encapsulation:* `Elevator.currentFloor` is private and only `step()` changes it — no external code can teleport an elevator.

### 5 — Basic code

```java
import java.util.*;

enum Direction { UP, DOWN, IDLE }
enum ElevatorState { IDLE, MOVING_UP, MOVING_DOWN, DOORS_OPEN, MAINTENANCE }

class Request {
    final int originFloor, destinationFloor;
    final boolean internal;                   // true = pressed inside the cabin
    Request(int origin, int destination, boolean internal) {
        this.originFloor = origin; this.destinationFloor = destination; this.internal = internal;
    }
    Direction direction() {
        return destinationFloor > originFloor ? Direction.UP : Direction.DOWN;
    }
}

class Elevator {
    private final int id;
    private int currentFloor = 0;
    private ElevatorState state = ElevatorState.IDLE;
    private final TreeSet<Integer> upTargets = new TreeSet<>();
    private final TreeSet<Integer> downTargets = new TreeSet<>(Comparator.reverseOrder());

    Elevator(int id) { this.id = id; }

    public int getId() { return id; }
    public int getCurrentFloor() { return currentFloor; }
    public ElevatorState getState() { return state; }
    public Direction getDirection() {
        if (state == ElevatorState.MOVING_UP) return Direction.UP;
        if (state == ElevatorState.MOVING_DOWN) return Direction.DOWN;
        return Direction.IDLE;
    }

    public void addTarget(int floor) {
        if (floor == currentFloor) { state = ElevatorState.DOORS_OPEN; return; }
        if (floor > currentFloor) upTargets.add(floor); else downTargets.add(floor);
        if (state == ElevatorState.IDLE) {
            state = floor > currentFloor ? ElevatorState.MOVING_UP : ElevatorState.MOVING_DOWN;
        }
    }

    /** One time step: move a single floor toward the next target, or open doors. */
    public void step() {
        if (state == ElevatorState.MAINTENANCE) return;

        if (state == ElevatorState.DOORS_OPEN) {         // doors close, then re-evaluate
            state = pickNextDirection();
            return;
        }
        if (state == ElevatorState.MOVING_UP) {
            if (upTargets.isEmpty()) { state = pickNextDirection(); return; }
            currentFloor++;
            if (upTargets.remove(currentFloor)) state = ElevatorState.DOORS_OPEN;
        } else if (state == ElevatorState.MOVING_DOWN) {
            if (downTargets.isEmpty()) { state = pickNextDirection(); return; }
            currentFloor--;
            if (downTargets.remove(currentFloor)) state = ElevatorState.DOORS_OPEN;
        }
    }

    /** SCAN behaviour: finish the current direction before reversing. */
    private ElevatorState pickNextDirection() {
        if (!upTargets.isEmpty())   return ElevatorState.MOVING_UP;
        if (!downTargets.isEmpty()) return ElevatorState.MOVING_DOWN;
        return ElevatorState.IDLE;
    }

    public int pendingStops() { return upTargets.size() + downTargets.size(); }
}

interface DispatchStrategy {
    Optional<Elevator> selectElevator(List<Elevator> elevators, Request request);
}

class NearestCarStrategy implements DispatchStrategy {
    public Optional<Elevator> selectElevator(List<Elevator> elevators, Request req) {
        return elevators.stream()
            .filter(e -> e.getState() != ElevatorState.MAINTENANCE)
            .min(Comparator.comparingInt(e -> score(e, req)));
    }
    /** Lower is better: distance, plus a penalty for elevators already heading away. */
    private int score(Elevator e, Request req) {
        int distance = Math.abs(e.getCurrentFloor() - req.originFloor);
        boolean movingAway = e.getDirection() != Direction.IDLE
                          && e.getDirection() != req.direction();
        return distance + (movingAway ? 100 : 0) + e.pendingStops();
    }
}

class ElevatorController {
    private final List<Elevator> elevators = new ArrayList<>();
    private DispatchStrategy strategy;                   // injected

    ElevatorController(int count, DispatchStrategy strategy) {
        for (int i = 0; i < count; i++) elevators.add(new Elevator(i));
        this.strategy = strategy;
    }

    public void setStrategy(DispatchStrategy s) { this.strategy = s; }

    public Optional<Elevator> requestElevator(Request req) {
        Optional<Elevator> chosen = strategy.selectElevator(elevators, req);
        chosen.ifPresent(e -> {
            e.addTarget(req.originFloor);
            e.addTarget(req.destinationFloor);
        });
        return chosen;
    }

    public void tick() { elevators.forEach(Elevator::step); }
}
```

**Follow-ups.**
- *"Optimize for energy."* → New `EnergyEfficientStrategy` preferring an already-moving elevator that passes the floor anyway. **Zero changes elsewhere** — say that out loud; it's the payoff of Strategy.
- *"Elevator breaks down mid-trip."* → Transition to MAINTENANCE, redistribute its targets through the controller, and stop dispatching to it.
- *"Rush hour, everyone going down."* → Zone the building, or bias the strategy to reposition idle cars to high floors. Mention that real systems use destination dispatch — you enter your floor in the lobby, and the system groups passengers.

---

## 2.6 Design a Vending Machine

The purest **State pattern** question that exists. If the interviewer wants to see you avoid a giant if/else, this is the one they pick.

### 1 — Clarify

- "Coins only, or cards too?"
- "Does it give change, and what if it can't make exact change?" (This is the interesting edge case — surface it yourself.)
- "Should a selection be refundable mid-transaction?"
- "Do I need inventory restocking and an admin mode?"

### 2 — Final idea

The machine is a state machine with four states: IDLE (waiting for money), HAS_MONEY (accepting selection), DISPENSING, and OUT_OF_STOCK. Each state is a class implementing the same interface, and **each state decides its own transitions** — so `VendingMachine` holds no conditionals at all. Inventory and coin change are separate collaborators.

### 3 — Entities and their functions

| Entity | Responsibility | Key methods |
|---|---|---|
| `VendingMachine` | Context: holds current state, inventory, balance | `insertCoin`, `selectProduct`, `dispense`, `refund` |
| `State` (interface) | Legal actions in this mode | `insertCoin`, `selectProduct`, `dispense`, `refund` |
| `IdleState`, `HasMoneyState`, `DispensingState`, `OutOfStockState` | Concrete behavior + transitions | implements |
| `Product` | Code, name, price in cents | getters |
| `Inventory` | Stock counts per slot | `has`, `deduct`, `restock` |
| `Coin` (enum) | NICKEL(5) … DOLLAR(100) | `getValue()` |
| `CoinDispenser` | Makes change greedily; reports when it can't | `canMakeChange(n)`, `dispense(n)` |

### 4 — OOP + design pattern

- **State** — the headline. Inserting a coin means something different in IDLE than in DISPENSING, and each state class encodes that. Compare it out loud to the alternative: a 60-line `if (currentState == ...)` block that grows every time a state is added.
- **Strategy** for `CoinDispenser` if they want a different change algorithm (greedy vs exact-change DP).
- **Singleton** for the machine.
- *Encapsulation:* `balance` is private; only state transitions modify it.
- *Polymorphism:* `currentState.insertCoin(...)` dispatches without the machine knowing which state it's in.

### 5 — Basic code

```java
import java.util.*;

enum Coin {
    NICKEL(5), DIME(10), QUARTER(25), DOLLAR(100);
    private final int cents;
    Coin(int cents) { this.cents = cents; }
    public int getValue() { return cents; }
}

class Product {
    final String code, name; final int priceCents;
    Product(String code, String name, int priceCents) {
        this.code = code; this.name = name; this.priceCents = priceCents;
    }
}

class Inventory {
    private final Map<String, Product> products = new HashMap<>();
    private final Map<String, Integer> counts = new HashMap<>();

    void restock(Product p, int qty) {
        products.put(p.code, p);
        counts.merge(p.code, qty, Integer::sum);
    }
    boolean hasStock(String code) { return counts.getOrDefault(code, 0) > 0; }
    Product get(String code)      { return products.get(code); }
    void deduct(String code)      { counts.computeIfPresent(code, (k, v) -> v - 1); }
    boolean isEmpty()             { return counts.values().stream().allMatch(v -> v == 0); }
}

interface State {
    void insertCoin(VendingMachine m, Coin c);
    void selectProduct(VendingMachine m, String code);
    void dispense(VendingMachine m);
    void refund(VendingMachine m);
}

class IdleState implements State {
    public void insertCoin(VendingMachine m, Coin c) {
        m.addBalance(c.getValue());
        m.setState(new HasMoneyState());
    }
    public void selectProduct(VendingMachine m, String code) {
        System.out.println("Insert money first.");
    }
    public void dispense(VendingMachine m) { System.out.println("Nothing selected."); }
    public void refund(VendingMachine m)   { System.out.println("No money to refund."); }
}

class HasMoneyState implements State {
    public void insertCoin(VendingMachine m, Coin c) { m.addBalance(c.getValue()); }

    public void selectProduct(VendingMachine m, String code) {
        if (!m.getInventory().hasStock(code)) { System.out.println("Out of stock."); return; }
        Product p = m.getInventory().get(code);
        if (m.getBalance() < p.priceCents) {
            System.out.println("Need " + (p.priceCents - m.getBalance()) + " more cents.");
            return;
        }
        int change = m.getBalance() - p.priceCents;
        if (!m.getDispenser().canMakeChange(change)) {
            System.out.println("Cannot make exact change — refunding.");
            refund(m);
            return;
        }
        m.setSelected(code);
        m.setState(new DispensingState());
        m.dispense();                                   // proceed immediately
    }

    public void dispense(VendingMachine m) { System.out.println("Select a product first."); }

    public void refund(VendingMachine m) {
        System.out.println("Refunding " + m.getBalance() + " cents.");
        m.resetBalance();
        m.setState(new IdleState());
    }
}

class DispensingState implements State {
    public void insertCoin(VendingMachine m, Coin c) { System.out.println("Please wait."); }
    public void selectProduct(VendingMachine m, String code) { System.out.println("Please wait."); }
    public void refund(VendingMachine m) { System.out.println("Too late to refund."); }

    public void dispense(VendingMachine m) {
        Product p = m.getInventory().get(m.getSelected());
        m.getInventory().deduct(p.code);
        int change = m.getBalance() - p.priceCents;
        System.out.println("Dispensing " + p.name + ", change " + change + " cents.");
        m.getDispenser().dispense(change);
        m.resetBalance();
        m.setState(m.getInventory().isEmpty() ? new OutOfStockState() : new IdleState());
    }
}

class OutOfStockState implements State {
    public void insertCoin(VendingMachine m, Coin c) { System.out.println("Machine empty."); }
    public void selectProduct(VendingMachine m, String code) { System.out.println("Machine empty."); }
    public void dispense(VendingMachine m) { }
    public void refund(VendingMachine m)   { m.resetBalance(); }
}

class CoinDispenser {
    private final Map<Coin, Integer> reserve = new EnumMap<>(Coin.class);
    CoinDispenser() { for (Coin c : Coin.values()) reserve.put(c, 20); }

    boolean canMakeChange(int cents) {
        int remaining = cents;
        List<Coin> desc = Arrays.asList(Coin.DOLLAR, Coin.QUARTER, Coin.DIME, Coin.NICKEL);
        for (Coin c : desc) {
            int use = Math.min(remaining / c.getValue(), reserve.get(c));
            remaining -= use * c.getValue();
        }
        return remaining == 0;
    }

    void dispense(int cents) {
        int remaining = cents;
        for (Coin c : Arrays.asList(Coin.DOLLAR, Coin.QUARTER, Coin.DIME, Coin.NICKEL)) {
            int use = Math.min(remaining / c.getValue(), reserve.get(c));
            reserve.put(c, reserve.get(c) - use);
            remaining -= use * c.getValue();
        }
    }
}

class VendingMachine {
    private State state = new IdleState();
    private final Inventory inventory = new Inventory();
    private final CoinDispenser dispenser = new CoinDispenser();
    private int balance = 0;
    private String selected;

    // Public API is four lines of pure delegation -- no conditionals anywhere.
    public void insertCoin(Coin c)          { state.insertCoin(this, c); }
    public void selectProduct(String code)  { state.selectProduct(this, code); }
    public void dispense()                  { state.dispense(this); }
    public void refund()                    { state.refund(this); }

    void setState(State s)      { this.state = s; }
    void addBalance(int cents)  { this.balance += cents; }
    void resetBalance()         { this.balance = 0; }
    int getBalance()            { return balance; }
    void setSelected(String c)  { this.selected = c; }
    String getSelected()        { return selected; }
    Inventory getInventory()    { return inventory; }
    CoinDispenser getDispenser(){ return dispenser; }
}
```

**The sentence that wins this round:** *"Notice `VendingMachine` has no if-statements — every branch lives in the state that owns it. Adding a MAINTENANCE state means adding one class and touching nothing else."*

**Follow-up.** *"Greedy change fails for some coin systems."* → Correct. Greedy is only optimal for canonical systems like US coins. For arbitrary denominations you need the Coin Change DP — link it back to §L2 of the coding pack.

---

## 2.7 Design a Logging Framework

Notable because it's one of the few problems that naturally uses **three patterns together** — a good showcase if the interviewer asks you to demonstrate pattern composition.

### 1 — Clarify

- "Levels — DEBUG through FATAL? Configurable minimum?"
- "Multiple destinations at once — console, file, remote?"
- "Should the format be pluggable — plain text, JSON?"
- "Async logging, or is synchronous acceptable?" (Async matters in production; say you'd use a bounded queue.)
- "Thread-safe? Log rotation?"

### 2 — Final idea

A `Logger` builds a `LogMessage` and passes it into a **chain** of `LogHandler`s. Each handler decides whether the level meets its threshold, formats via an injected `Formatter`, writes to its own destination, and then passes the message down the chain. A `LoggerFactory` returns configured singletons by name.

### 3 — Entities and their functions

| Entity | Responsibility | Key methods |
|---|---|---|
| `LogLevel` (enum) | DEBUG < INFO < WARN < ERROR < FATAL, ordered | `isAtLeast(other)` |
| `LogMessage` | Immutable: level, text, timestamp, thread, logger name | getters |
| `Formatter` (interface) | Message → string | `format(msg)` |
| `PlainFormatter`, `JsonFormatter` | Concrete formats | implements |
| `LogHandler` (abstract) | One link in the chain; threshold + destination | `handle(msg)`, `setNext(h)` |
| `ConsoleHandler`, `FileHandler`, `RemoteHandler` | Concrete sinks | `write(text)` |
| `Logger` | Public API | `debug`, `info`, `warn`, `error` |
| `LoggerFactory` | Named logger registry | `getLogger(name)` |

### 4 — OOP + design pattern

- **Chain of Responsibility** for the handler chain — each handler processes if relevant, then delegates onward. Adding a remote sink means inserting a link.
- **Strategy** for `Formatter` — swap text for JSON with no handler changes.
- **Singleton / Factory** for `LoggerFactory` — one logger instance per name.
- *Template Method* (bonus): `LogHandler.handle()` is final and defines the sequence (check level → format → write → pass on), while subclasses only implement `write()`. Naming Template Method here is a nice extra.
- *Abstraction:* callers say `log.info("...")` and know nothing about sinks.

### 5 — Basic code

```java
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

enum LogLevel {
    DEBUG, INFO, WARN, ERROR, FATAL;
    boolean isAtLeast(LogLevel min) { return this.ordinal() >= min.ordinal(); }
}

final class LogMessage {
    final LogLevel level; final String text; final Instant time;
    final String threadName, loggerName;
    LogMessage(LogLevel level, String text, String loggerName) {
        this.level = level; this.text = text; this.time = Instant.now();
        this.threadName = Thread.currentThread().getName(); this.loggerName = loggerName;
    }
}

interface Formatter { String format(LogMessage m); }

class PlainFormatter implements Formatter {
    public String format(LogMessage m) {
        return String.format("%s [%s] %s %s - %s",
                m.time, m.threadName, m.level, m.loggerName, m.text);
    }
}

class JsonFormatter implements Formatter {
    public String format(LogMessage m) {
        return String.format("{\"ts\":\"%s\",\"level\":\"%s\",\"logger\":\"%s\",\"msg\":\"%s\"}",
                m.time, m.level, m.loggerName, m.text.replace("\"", "\\\""));
    }
}

abstract class LogHandler {
    private final LogLevel minLevel;
    private final Formatter formatter;
    private LogHandler next;

    protected LogHandler(LogLevel minLevel, Formatter formatter) {
        this.minLevel = minLevel; this.formatter = formatter;
    }

    public LogHandler setNext(LogHandler next) { this.next = next; return next; }

    /** Template Method: fixed sequence, subclasses only supply write(). */
    public final void handle(LogMessage m) {
        if (m.level.isAtLeast(minLevel)) write(formatter.format(m));
        if (next != null) next.handle(m);          // Chain of Responsibility
    }

    protected abstract void write(String formatted);
}

class ConsoleHandler extends LogHandler {
    ConsoleHandler(LogLevel min, Formatter f) { super(min, f); }
    protected void write(String s) { System.out.println(s); }
}

class FileHandler extends LogHandler {
    private final String path;
    FileHandler(LogLevel min, Formatter f, String path) { super(min, f); this.path = path; }
    protected synchronized void write(String s) {
        // Real impl: buffered writer + size-based rotation.
        System.out.println("[file:" + path + "] " + s);
    }
}

class Logger {
    private final String name;
    private final LogHandler chainHead;
    Logger(String name, LogHandler chainHead) { this.name = name; this.chainHead = chainHead; }

    private void log(LogLevel level, String msg) {
        chainHead.handle(new LogMessage(level, msg, name));
    }
    public void debug(String m) { log(LogLevel.DEBUG, m); }
    public void info(String m)  { log(LogLevel.INFO,  m); }
    public void warn(String m)  { log(LogLevel.WARN,  m); }
    public void error(String m) { log(LogLevel.ERROR, m); }
}

class LoggerFactory {
    private static final Map<String, Logger> LOGGERS = new ConcurrentHashMap<>();
    private static LogHandler defaultChain;

    static {
        ConsoleHandler console = new ConsoleHandler(LogLevel.DEBUG, new PlainFormatter());
        console.setNext(new FileHandler(LogLevel.WARN, new JsonFormatter(), "app.log"));
        defaultChain = console;             // console gets everything, file only WARN+
    }

    public static Logger getLogger(String name) {
        return LOGGERS.computeIfAbsent(name, n -> new Logger(n, defaultChain));
    }
}
```

**Follow-up.** *"Logging is blocking my request thread."* → Put a bounded `BlockingQueue<LogMessage>` in front, with a consumer thread draining it into the chain. Then discuss the real question: **what do you do when the queue fills?** Drop the oldest, drop the newest, or block the producer. Each is a defensible choice with a different failure mode, and naming the trade-off is the answer they want.

---

## 2.8 Design Amazon Locker (Package Pickup)

An Amazon-specific favorite, and a good one because the matching logic is genuinely non-trivial.

### 1 — Clarify

- "Locker sizes — small, medium, large? Can a small package go in a large slot?"
- "How long is a package held before it's returned to the warehouse?"
- "Is the pickup code single-use? Time-limited?"
- "One location or many? Should I handle finding the nearest location?"
- "Can a customer request a specific locker location?"

### 2 — Final idea

A `LockerLocation` owns `Locker`s bucketed by size. Assigning a package finds the **smallest free locker that fits**, generates a one-time code with an expiry, and records an `Assignment`. Pickup validates the code and expiry, opens the locker, and frees it. A background job reclaims expired assignments and returns those packages.

### 3 — Entities and their functions

| Entity | Responsibility | Key methods |
|---|---|---|
| `LockerSize` (enum) | SMALL / MEDIUM / LARGE, ordered by capacity | — |
| `Package` | Id, dimensions, recipient | `getRequiredSize()` |
| `Locker` | Owns occupancy, opens and closes | `assign(pkg)`, `open(code)`, `release()` |
| `Assignment` | Package ↔ locker ↔ code ↔ expiry | `isExpired()`, `matches(code)` |
| `CodeGenerator` (interface) | Produces a pickup code | `generate()` |
| `LockerLocation` | Finds a fitting locker at this site | `findAvailable(size)` |
| `LockerService` | Orchestrates assign, pickup, expiry sweep | `assignLocker`, `pickup`, `reclaimExpired` |
| `NotificationService` | Tells the customer the code | `notify(assignment)` |

### 4 — OOP + design pattern

- *Encapsulation:* `Locker.currentPackage` is private; `assign()` throws if occupied, so double-booking is structurally impossible.
- *Polymorphism / Strategy:* `CodeGenerator` is an interface — numeric today, QR tomorrow.
- **Observer** for `NotificationService` — the service publishes an assignment event and email/SMS subscribers react independently.
- **Factory** if locker types diverge (refrigerated, oversized).
- *Composition:* a location **has** lockers.
- **Single Responsibility in action:** `LockerService` orchestrates, `Locker` manages its own state, `NotificationService` communicates. Point out that no class does two of those.

### 5 — Basic code

```java
import java.time.Duration;
import java.time.Instant;
import java.util.*;

enum LockerSize { SMALL, MEDIUM, LARGE }

class Package {
    final String id; private final LockerSize requiredSize; final String recipientId;
    Package(String id, LockerSize size, String recipientId) {
        this.id = id; this.requiredSize = size; this.recipientId = recipientId;
    }
    LockerSize getRequiredSize() { return requiredSize; }
}

class Locker {
    private final String id; private final LockerSize size;
    private Package currentPackage; private boolean open;

    Locker(String id, LockerSize size) { this.id = id; this.size = size; }

    String getId() { return id; }
    LockerSize getSize() { return size; }
    boolean isFree() { return currentPackage == null; }
    boolean canFit(Package p) { return isFree() && size.ordinal() >= p.getRequiredSize().ordinal(); }

    synchronized void assign(Package p) {
        if (!canFit(p)) throw new IllegalStateException("Locker " + id + " cannot take " + p.id);
        this.currentPackage = p;
    }
    synchronized Package open() { this.open = true; return currentPackage; }
    synchronized void release() { this.currentPackage = null; this.open = false; }
}

class Assignment {
    final String code; final Locker locker; final Package pkg;
    final Instant expiresAt;
    Assignment(String code, Locker locker, Package pkg, Duration holdFor) {
        this.code = code; this.locker = locker; this.pkg = pkg;
        this.expiresAt = Instant.now().plus(holdFor);
    }
    boolean isExpired() { return Instant.now().isAfter(expiresAt); }
    boolean matches(String attempt) { return code.equals(attempt); }
}

interface CodeGenerator { String generate(); }

class NumericCodeGenerator implements CodeGenerator {
    private final Random rnd = new Random();
    public String generate() { return String.format("%06d", rnd.nextInt(1_000_000)); }
}

class LockerLocation {
    final String id; private final List<Locker> lockers = new ArrayList<>();
    LockerLocation(String id) { this.id = id; }
    void addLocker(Locker l) { lockers.add(l); }

    /** Smallest fitting locker, so large lockers stay free for large packages. */
    Optional<Locker> findAvailable(Package p) {
        return lockers.stream().filter(l -> l.canFit(p))
                      .min(Comparator.comparingInt(l -> l.getSize().ordinal()));
    }
}

interface AssignmentListener { void onAssigned(Assignment a); }

class LockerService {
    private final List<LockerLocation> locations = new ArrayList<>();
    private final Map<String, Assignment> byCode = new HashMap<>();
    private final CodeGenerator codes;
    private final Duration holdDuration;
    private final List<AssignmentListener> listeners = new ArrayList<>();

    LockerService(CodeGenerator codes, Duration holdDuration) {
        this.codes = codes; this.holdDuration = holdDuration;
    }

    void addLocation(LockerLocation l) { locations.add(l); }
    void subscribe(AssignmentListener l) { listeners.add(l); }

    public synchronized Optional<Assignment> assignLocker(Package pkg, String locationId) {
        for (LockerLocation loc : locations) {
            if (!loc.id.equals(locationId)) continue;
            Optional<Locker> free = loc.findAvailable(pkg);
            if (free.isEmpty()) return Optional.empty();
            Locker locker = free.get();
            locker.assign(pkg);
            Assignment a = new Assignment(codes.generate(), locker, pkg, holdDuration);
            byCode.put(a.code, a);
            listeners.forEach(l -> l.onAssigned(a));         // Observer
            return Optional.of(a);
        }
        return Optional.empty();
    }

    public synchronized Optional<Package> pickup(String code) {
        Assignment a = byCode.get(code);
        if (a == null || a.isExpired()) return Optional.empty();
        Package p = a.locker.open();
        a.locker.release();
        byCode.remove(code);                                  // single-use code
        return Optional.ofNullable(p);
    }

    /** Background sweep: return unclaimed packages and free their lockers. */
    public synchronized List<Package> reclaimExpired() {
        List<Package> reclaimed = new ArrayList<>();
        Iterator<Map.Entry<String, Assignment>> it = byCode.entrySet().iterator();
        while (it.hasNext()) {
            Assignment a = it.next().getValue();
            if (a.isExpired()) { reclaimed.add(a.pkg); a.locker.release(); it.remove(); }
        }
        return reclaimed;
    }
}
```

**Follow-ups.**
- *"No locker free at the requested location."* → Search nearby locations by distance (a geo index or simple radius scan) and offer alternatives, or queue the package for the next free slot.
- *"Code collisions."* → Six digits is only a million codes. Either scope uniqueness per location, check on generate and retry, or use a longer code. Noticing this unprompted is a strong Dive Deep signal.
- *"Returns — customer drops a package in."* → Same flow reversed, with a returns-specific assignment type. Mention that `Assignment` would gain a direction field rather than being subclassed.

---

# 3. High-Level System Design (the L4 depth)

**Calibration.** Full distributed design is an SDE-II+ round. At L4 you may get a light version, or the Bar Raiser may probe one. What's expected is **structured thinking and honest trade-offs**, not a production architecture. Don't try to perform seniority you don't have — say "I haven't built this at scale, but here's how I'd reason about it" and then reason well. That reads far better than confident hand-waving.

**A 5-step frame that fits 20 minutes:**
1. **Requirements** — functional (what it does), non-functional (scale, latency, consistency). Ask, don't assume.
2. **Back-of-envelope** — QPS, storage, bandwidth. One or two numbers, not a spreadsheet.
3. **API + data model** — the endpoints and the core table or key layout. This grounds everything.
4. **Architecture** — the boxes, drawn once, walked through with one request's path.
5. **Deep dive on one thing** — let the interviewer pick, or offer the hardest part yourself.

**The CAP sentence to have ready:** *"Under a network partition you choose availability or consistency. S3 chose strong read-after-write consistency for new objects, which is a deliberate trade against some availability in a partition. DynamoDB lets the caller choose per-request."*

---

## 3.1 Design S3 (a Blob / Object Store) — the flagship

### 1 — Clarify

- "What scale — objects, total bytes, requests per second?"
- "Max object size? Do I need multipart upload for large objects?"
- "Consistency: strong read-after-write, or is eventual acceptable?"
- "What durability target?" (S3 advertises eleven nines — 99.999999999%.)
- "Is versioning and lifecycle tiering in scope, or just PUT/GET/DELETE/LIST?"

### 2 — Final idea

Split **metadata** from **data**. Metadata (key → version list → chunk locations) lives in a partitioned, replicated key-value index. Data is split into fixed-size chunks, erasure-coded, and spread across independent failure domains in multiple availability zones. A stateless request-routing tier authenticates, looks up metadata, and streams chunks. Durability comes from redundancy plus continuous background verification; consistency comes from making the metadata commit the single ordering point.

### 3 — Components and their functions

| Component | Function |
|---|---|
| Request router / front end | TLS termination, auth (SigV4), request validation, rate limiting per bucket |
| Metadata service | Key → versions → chunk map. Partitioned by hashed bucket+key; strongly consistent within a partition |
| Placement service | Chooses which storage nodes hold each chunk, respecting failure-domain spread |
| Storage nodes | Store immutable chunks on disk; never mutate, only write and delete |
| Erasure coding layer | Splits a chunk into k data + m parity fragments; any k reconstruct the whole |
| Repair / audit service | Continuously reads checksums, detects bit rot and lost fragments, rebuilds |
| Lifecycle engine | Applies age-based transition and expiry rules |
| Event notification | Publishes object-created/removed events to queues and functions |

### 4 — Key design decisions (the "pattern" layer for HLD)

- **Separate metadata from data.** Metadata is small, hot, and needs transactions. Data is huge, cold, and needs throughput. Different systems, different scaling curves. This is *the* insight of the design — lead with it.
- **Immutability.** Objects are never edited in place; a PUT writes new chunks and flips a metadata pointer. That's what makes strong read-after-write consistency achievable: the metadata commit is atomic, and readers see either the old pointer or the new one, never a half-written object.
- **Erasure coding over replication.** 3× replication costs 200% overhead. A (10,4) erasure code tolerates 4 simultaneous fragment losses at only 40% overhead. Trade-off: reconstruction on read costs CPU and network. Naming this comparison specifically is high-signal.
- **Consistent hashing** for metadata partitioning, so adding capacity moves ~1/N of keys instead of remapping everything.
- **Flat keyspace.** No directories. `ListObjectsV2` synthesizes hierarchy with prefix + delimiter over a sorted index — connect this back to §2.2 and the trie problems.

### 5 — The parts to be able to sketch

**PUT path:** authenticate → chunk the stream → erasure-code each chunk → write fragments in parallel to placement-chosen nodes → wait for a durable quorum → **atomically commit metadata** (this is the commit point) → return 200 with an ETag.

**GET path:** authenticate → metadata lookup for the current version → fetch k fragments in parallel → reconstruct → stream out. Slow fragment? Read extra fragments and use whichever k return first — hedged reads.

**Multipart upload:** client initiates and gets an upload id; parts upload independently (and can be retried individually); `complete` validates that all parts are present and stitches the chunk list. Part boundaries are an **interval problem** — say so, it ties your design answer to your coding answer.

**Back-of-envelope worth doing out loud:** 100 PB of data at (10,4) erasure coding = 140 PB raw. At 20 TB per drive that's 7,000 drives, and at ~50 drives per host, ~140 hosts per copy of the keyspace — before spare capacity and multi-AZ spread. Rough numbers are fine; showing the method is the point.

**Failure questions they'll ask.** Whole AZ dies → spread fragments so any single AZ holds fewer than m fragments, keeping every object readable. Silent bit rot → per-fragment checksums verified on read *and* by a continuous background scrubber. Hot key → cache in front, and shard the object across more nodes.

---

## 3.2 Design a URL Shortener

The most common warm-up HLD. Prized because it's small enough to actually finish.

**Clarify.** Custom aliases? Link expiry? Analytics on clicks? Read:write ratio (it's heavily read-skewed, typically 100:1)? How many URLs per day?

**Final idea.** A write path that assigns a unique short code and stores the mapping; a read path that resolves the code and issues an HTTP 301/302 redirect. The only real design question is **how to generate codes without collisions across many hosts**.

**Components.** API service · code generator · key-value store (code → long URL) · cache in front of reads · analytics pipeline (async, off the redirect path) · optional CDN.

**Key decisions.**
- **Code generation — pick one and defend it.** (a) Hash the URL and take the first 7 base-62 characters; simple, but needs collision handling. (b) A global counter encoded in base 62; guarantees uniqueness but the counter is a bottleneck and codes are guessable. (c) **Pre-allocated ranges** — each host claims a block of a million ids from a coordination service and hands them out locally. This is the best answer: no per-request coordination, no collisions.
- **62⁷ ≈ 3.5 trillion codes** — seven characters is plenty. Do that arithmetic out loud.
- **301 vs 302.** A 301 is cached by browsers, saving you traffic but destroying your click analytics. A 302 gives you every click. **The choice depends on whether analytics is a requirement** — that sentence is what they're listening for.
- Analytics must be asynchronous (fire an event onto a queue), never inline in the redirect.

**Deep dive to offer.** Cache design: an LRU in front of the store, with a 100:1 read ratio meaning a high hit rate. Note the cold-start thundering herd and mention request coalescing.

---

## 3.3 Design a Distributed Rate Limiter

The natural scale-up of §2.4, and a likely follow-up if you get the LLD version.

**Clarify.** Per user, per API key, or per IP? What limit and window? Is brief over-admission acceptable, or must the limit be hard? How many gateway hosts?

**Final idea.** Keep counters in a central fast store (Redis) so all hosts see the same state, and make check-and-decrement **atomic** with a Lua script. Accept a small amount of over-admission during Redis failover rather than failing requests closed.

**Components.** Gateway hosts running the limiter client · Redis cluster sharded by client key · config service for per-client limits · a local in-process fallback limiter.

**Key decisions.**
- **Atomicity is the whole problem.** A separate GET then SET races across hosts. One Lua script that reads, decides, and writes runs atomically inside Redis.
- **Central counters vs local quotas.** Central is accurate but adds a network hop to every request and a hard dependency. Local quotas of `limit/N` per host need no coordination but waste capacity when traffic is uneven — you can rebalance periodically. **Say both and pick one for the stated requirements.**
- **Fail open or fail closed?** If Redis is down, do you admit everything or reject everything? For a public API you usually fail open with a conservative local limiter, because rejecting all traffic turns a dependency blip into a full outage. State the choice and the reason; there is no universally right answer and they know it.

---

## 3.4 Design a Large File Upload Service (multipart, resumable)

Highly relevant to S3 and a good pick if you're given a choice of topic.

**Clarify.** Maximum file size? Must uploads resume after a network drop? Do you need integrity verification? Is the client a browser, a mobile app, or an SDK?

**Final idea.** Split the file client-side into fixed-size parts. Each part uploads independently against an upload id, can be retried on its own, and carries a checksum. When all parts are present, a `complete` call validates and assembles. The client can query which parts already landed, which is what makes resume work.

**Components.** Initiate/complete API · part-upload endpoints issuing pre-signed URLs so bytes go straight to storage without transiting your service · upload-session metadata store · checksum verifier · a garbage collector for abandoned sessions.

**Key decisions.**
- **Pre-signed URLs.** The client uploads directly to storage using a short-lived signed URL. Your service never handles the bytes — that's the difference between a service that scales and one that doesn't.
- **Part size trade-off.** Small parts mean more requests and more metadata but cheaper retries. Large parts mean fewer requests but an expensive retry. Something like 8–16 MB is a common middle. Reason it out rather than reciting a number.
- **Idempotency.** Re-uploading part 5 must overwrite cleanly, not append. Keying by `(uploadId, partNumber)` gives you that for free.
- **Abandoned uploads leak storage.** A lifecycle rule aborts incomplete uploads after N days. Volunteering this shows operational thinking — it's a real S3 feature and a real source of surprise bills.
- **Integrity.** Per-part checksum plus a composite checksum over the assembled object.

---

## 3.5 Design a Distributed Cache

**Clarify.** Cache size and item size? Eviction policy? Is stale data acceptable, and for how long? Write-through, write-back, or cache-aside? How do you invalidate?

**Final idea.** Shard the keyspace across nodes with **consistent hashing** so adding or removing a node remaps only ~1/N of keys. Each node runs the single-node cache from §2.3. Clients hash the key to find the owning node directly, keeping the read path to one hop.

**Key decisions.**
- **Consistent hashing with virtual nodes.** Plain modulo hashing remaps nearly everything when N changes — a guaranteed cache stampede. Consistent hashing places nodes on a ring and each key goes to the next node clockwise. **Virtual nodes** (each physical node appearing at many ring positions) fix the load imbalance that plain consistent hashing leaves behind. Explaining *why* virtual nodes exist is the differentiator here.
- **Cache-aside vs write-through.** Cache-aside (app checks cache, on miss reads the database and populates) is simplest and most common; the cost is a stale window. Write-through keeps the cache correct but adds latency to every write.
- **Thundering herd.** When a hot key expires, thousands of requests miss simultaneously and hammer the database. Fixes: a per-key lock so one request repopulates while others wait; or probabilistic early refresh before expiry. Naming this problem unprompted is strong.
- **Hot keys** break sharding, because one key can exceed one node's capacity. Fix by replicating hot keys to several nodes, or adding a small local cache on each client.

---

## 3.6 Design a Metrics & Monitoring Pipeline

Relevant because every AWS team runs on operational metrics, and it's a natural fit for a storage team.

**Clarify.** How many hosts emitting, at what interval? What retention? Query patterns — recent dashboards, or long historical ranges? Alerting latency requirements?

**Final idea.** Agents on each host batch metrics and push to an ingestion tier, which writes into a time-series store partitioned by time and by metric. Recent data stays at full resolution in hot storage; older data is downsampled and rolled to cold storage. Alerting evaluates rules against the recent window continuously.

**Components.** Host agents · ingestion service (batched, back-pressured) · a message queue to absorb spikes · time-series store · downsampling/rollup jobs · query service · alerting engine.

**Key decisions.**
- **Push vs pull.** Push scales to ephemeral hosts that come and go; pull (Prometheus-style) gives the collector control and easier failure detection. Say which you'd pick and why.
- **Time-partitioned storage.** Almost all queries are "recent," so partitioning by time makes old data trivially droppable and recent queries fast.
- **Downsampling.** Second-resolution data for 24 hours, minute for 30 days, hour for a year. Storage drops by orders of magnitude and nobody queries second-granularity data from last March.
- **Cardinality is the real killer.** Every unique tag combination is a separate series. A tag containing request ids will destroy the system. Volunteering this is the single most credible thing you can say about metrics systems.

---

# 4. Running the design round

## The clock

For a 45-minute round with ~15 minutes of LP, you have roughly 30:

| Minutes | What you're doing |
|---|---|
| 0–3 | Clarify. Ask 3–5 questions. Write the requirements where they can see them. |
| 3–5 | **State your scope and get agreement.** "I'll build X and Y, and stub Z. Sound right?" |
| 5–10 | Name your classes or components out loud. Sketch, don't diagram. |
| 10–25 | Code the core. Talk while you type. |
| 25–30 | Walk one scenario end to end. Name what you'd add with more time. |

**The scope-agreement step at minute 3 is the highest-value part of the round.** Candidates who skip it build something the interviewer didn't want and run out of time.

## Ten mistakes that sink L4 design rounds

1. **Coding before agreeing on scope.** The number-one cause of a failed round.
2. **Drawing UML for 20 minutes.** They want classes and methods; one report is explicit about this.
3. **Pattern-stuffing.** Five patterns in a parking lot reads as memorization, not judgment.
4. **God classes.** A `ParkingLot` that also prices, prints receipts, and sends emails fails Single Responsibility on sight.
5. **Public mutable fields.** Encapsulation is the pillar this round is literally named after.
6. **`instanceof` chains.** If you're switching on type, you've skipped polymorphism.
7. **No mention of thread safety.** Even "single-threaded for now, but here's where I'd lock" scores.
8. **Ignoring the follow-up hint.** "How would you add a new pricing model?" means *your design isn't extensible enough.* Refactor toward Strategy right there rather than defending what you wrote.
9. **Silence while coding.** They're grading your reasoning, and they can't see it.
10. **Not finishing anything.** A small working design beats an ambitious half-built one. Amazon interviewers reward working over optimal — cut scope early and out loud.

## Six sentences worth memorizing

- *"Before I start — can I confirm the scope? I'll build A and B, and stub C behind an interface."*
- *"I'm using composition here, not inheritance, because a lot **has** floors rather than **is** a floor."*
- *"I'll put pricing behind a Strategy interface so a new rate card is a new class, not an edit to existing code."*
- *"This is O(n) right now with a linear scan. I'd swap in a priority queue per size bucket to get O(log n) — want me to do that, or move on?"*
- *"For thread safety I'd start with a single lock on this method. If contention became a problem I'd shard by key hash into independently-locked segments."*
- *"That's the core working. With more time I'd add X, Y, and Z — which of those would you like me to go deeper on?"*

That last one hands the interviewer the wheel at exactly the moment they want it, and it converts an unfinished design into a deliberate one.
