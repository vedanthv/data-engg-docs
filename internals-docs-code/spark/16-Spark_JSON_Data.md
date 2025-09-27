### Lecture 11: Working with JSON Data in Spark

![image](https://github.com/user-attachments/assets/09ce5719-db12-446c-8247-9495ea979768)

Two types of JSON notation:

- Line Delimited JSON
![image](https://github.com/user-attachments/assets/95b248fd-491a-4083-963f-102489848154)

- Multi Line JSON
![image](https://github.com/user-attachments/assets/91f43e31-58a1-4443-a5c2-fc376ef61c38)

```json
[
{
  "name": "Manish",
  "age": 20,
  "salary": 20000
},
{
  "name": "Nikita",
  "age": 25,
  "salary": 21000
},
{
  "name": "Pritam",
  "age": 16,
  "salary": 22000
},
{
  "name": "Prantosh",
  "age": 35,
  "salary": 25000
},
{
  "name": "Vikash",
  "age": 67,
  "salary": 40000
}
]
```

Line Delimited JSON is more efficient in terms of performance because the compiler knows that each line has one JSON record whereas in multiline json the compiler needs to keept track of where the record ends and the next one starts.

#### Different number of keys in each line

![image](https://github.com/user-attachments/assets/8aeeeb0a-906f-44a5-b3a0-a7c5c8d28e31)

Here what happens is that the line with the extra key has the value while for the rest its null
![image](https://github.com/user-attachments/assets/1fc8a438-c9f8-4d7e-8fbb-82c8ec73f167)

#### Multiline Incorrect JSON

We dont pass a list here rather its just dictionaries
```json
{
  "name": "Manish",
  "age": 20,
  "salary": 20000
},
{
  "name": "Nikita",
  "age": 25,
  "salary": 21000
},
{
  "name": "Pritam",
  "age": 16,
  "salary": 22000
},
{
  "name": "Prantosh",
  "age": 35,
  "salary": 25000
},
{
  "name": "Vikash",
  "age": 67,
  "salary": 40000
}
```
When we process the json it just reads the first dictionary as a record and the rest is not processed.

![image](https://github.com/user-attachments/assets/6b25b6f2-8eda-466d-affc-08c0fed2f551)

#### Corrupted Records

We dont need to define ```_corrupted_record``` in the schema, it will add the column on its ownn

![image](https://github.com/user-attachments/assets/60f6c31e-6174-40ab-ba71-e3f0070a01fa)