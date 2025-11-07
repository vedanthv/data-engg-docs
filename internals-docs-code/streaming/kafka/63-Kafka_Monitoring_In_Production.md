# Kafka Monitoring In Production

Kafka’s Java clients include JMX metrics that allowmonitoring client-side status and events. For the producers,the two metrics most important for reliability are error-rateand retry-rate per record (aggregated). Keep an eye onthose, since error or retry rates going up can indicate anissue with the system. Also monitor the producer logs forerrors that occur while sending events that are logged atWARN level, and say something along the lines of “Got errorproduce response with correlation id 5689 on topic partition [topic-1,3], retrying (two attempts left). Error: …”When we see events with 0 attempts left, the producer is running out of retries. 

In Chapter 3 we discussed how to configure delivery.timeout.ms and retries to improve the error handling in the producer and avoid running out of retries prematurely. Of course, it is always better to solve the problem that caused the errors in the first place. ERROR level log messages on the producer are likely to indicate that sending the message failed completely due to non retriable error, a retriable error that ran out of retries,or a timeout. When applicable, the exact error from thebroker will be logged as well.


