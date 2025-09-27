### Lecture 32 : Dynamic Partition Pruning

![image](https://github.com/user-attachments/assets/f3fec4e7-fb1c-4df7-8fcf-3a5603f37145)

In below code we have a filter applied to select only 19th April 2023 data,

![image](https://github.com/user-attachments/assets/c2b31884-ff92-4899-94b6-0e2eca6036e9)

Below we can see that only one file that is for 19th April 2023 is read, not all of them.

![image](https://github.com/user-attachments/assets/6145f2e9-ad56-4d9f-bff0-cc1d5cddc47d)

![image](https://github.com/user-attachments/assets/b0aeae59-6aad-4522-b88c-d48ed168b340)

#### DPP with 2 tables

![image](https://github.com/user-attachments/assets/41fd14e0-7e73-4e27-a646-1d9be439c64c)

Partition pruning does not happen on first table but will happen on table 2. Dynamic Partition Pruning helps us to update filter on runtime.

Two conditions:

- Data should be partitioned.
- 2nd Table should be broadcasted.

![image](https://github.com/user-attachments/assets/2c7f3104-572f-4104-b0d7-ee0ca2685ab8)

![image](https://github.com/user-attachments/assets/687e08bf-21bd-4c68-a4e1-4547f72de828)

**Without Dynamic Partition Pruning**

Total 123 files read from first table not one like previous case.

![image](https://github.com/user-attachments/assets/bb08d05b-3504-40d7-afee-92be1b96c4c6)

**With Dynamic Partition Pruning**

![image](https://github.com/user-attachments/assets/af82cde4-1d28-40a8-b7d5-317b14b7a2c8)

![image](https://github.com/user-attachments/assets/177581ed-bda5-4cba-8bc4-e7412dc3dbc8)

The smaller dimdate table is broadcasted and hash join performed. Only 3 files are read this time.

![image](https://github.com/user-attachments/assets/43fab357-56c8-4ce2-bc4d-b88c7c226488)

At runtime a subquery is run...

![image](https://github.com/user-attachments/assets/f0ce0f0a-e8de-484d-981d-780a21c90d53)

![image](https://github.com/user-attachments/assets/c50c043b-6029-4721-9247-452ffb0492c4)

Now because of the runtime filter only 4 partitions are read/scanned.