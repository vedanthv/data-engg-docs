### Lecture 18: Job, Stage and Tasks

![image](https://github.com/user-attachments/assets/f54725bf-2e81-4b73-a65c-97cb449887c7)

- One Application is created.
- One job is created per action.
- One stage is defined for every transformation like filter.
- Task is the actually activity on the data that's happening.

![image](https://github.com/user-attachments/assets/025a67b4-2ced-4ad9-a23a-eaa6d65f349c)

#### Example of Job,Action and Task

![image](https://github.com/user-attachments/assets/b232dc8d-ff27-4650-92ca-7c3b912b5132)

#### Complete flow diagram
![image](https://github.com/user-attachments/assets/4e07a77b-8885-46a7-8793-53d7dd3f5f59)

Every job has minimum one stage and one task.

![image](https://github.com/user-attachments/assets/96990346-8429-41e7-ac94-f11855baa9de)
Repartition to filter is one job because we dont hit an action in between.

Every wide dependency transformation has its own stage. All narrow dependency transformations come in one stage as a DAG.

![image](https://github.com/user-attachments/assets/d9c8d425-892c-4ac0-bb6e-930bc9f51a32)

#### How do tasks get created? [Read and Write Exchange]

![image](https://github.com/user-attachments/assets/4d47470c-a3bc-4656-9b1a-7f718edd2c47)

- The repartition stage actually is a wide dependency transformation and creates two partitions from one, its a Write exchange of data.
- Now the filter and select stage reads this repartitioned data(**Read exchange**) and filter creates two tasks because we have two partitions.
- Next we need to find out how many folks earn > 90000 and age > 25 so we need to do a groupby that's a wide dependency transformation and it creates another stage. By default there are 200 partitions created.
- So some partitions may have data and some wont.

![image](https://github.com/user-attachments/assets/ec5734b2-3985-4fdd-abc4-4933e890e080)