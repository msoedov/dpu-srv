
## Assignment

Your task is to accomplish the following:

> - Document how you would store and return real-time count for spaces.

I took an approach where I store real-time and historic time series data in two separate DB tables.
This decision provides a trade-off to simplify aggregation queries and improve the scalability of DB since these two tables could be indexed, scaled, and federated to different db instances. However, this approach requires an additional 2 writes per the DPU event. 


> - Document how you would store and return historical count for spaces.

Historical data described in Events model. 


> - Prototype an API endpoint that yields the current count of a given space at a given point in time.

[x] Done

> - Describe the technologies you would use in production to handle this workload at scale (100,000 DPUs).

100,000 DPUs - is about 1GB of stored db data for DPU records (*1kb per records) + 1GB of spaces-doors data - this super easy to store in any relation sql db

With average 1 event per minute per dpu - this produces roughly 1.7k events/ sec or 1.5 GB of historic data / 24h | 0.5 TB of data / yearly

With the current approach if we cache all select and it's gonna require only 2 inserts / 2 updates per event. Given 4 * 1.7 ~ 6.8k inserts per sec this is something that even a single instance of Postgres can handle (I would test it though :)) . 

What we can do is to use Kafka/streaming transport to deliver dpu events. With this approach, dpu can push batches of events from the device and db consumer can process events in batches for more efficient db inserts. On top of that, we could partition Kafka consumer groups by space/dpu id and use database partitioning by space id/company id to achieve even x1000 higher throughput. 
Tradeoff: However, with Kafka batching, we might increase the latency of real-time data updates. We need to properly handle delivery at-least once cases for events.


Additionally, it's possible to use KV storage for RealtimeSpaceData and column-based nosql for Events tables (Cassandra/DynamoDB)






## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python

```

## Deployment

```
zappa update dev
```

## Jira
