### Window functions in Spark

#### Rank vs Dense Rank

![image](https://github.com/user-attachments/assets/73665356-9370-45b3-9499-d97cf200d464)

Dense rank does not leave any gaps between the ranks.

![image](https://github.com/user-attachments/assets/d25268ac-6ef9-4367-b151-08bcb14d320d)

#### Lead and Lag

![image](https://github.com/user-attachments/assets/60cc0b87-5d07-4873-ba7d-d1766d136dbb)

![image](https://github.com/user-attachments/assets/406bcb15-c4cd-4837-8ec9-694fe652b754)

#### Range and Row Between

![image](https://github.com/user-attachments/assets/2880cef0-ceee-4a15-a1e3-d80110fe0582)

Q1

![image](https://github.com/user-attachments/assets/7280b56c-aa7e-4521-8b0b-d4bb3c58efbd)

Using first and last functions let's try to acheive this.

Data:

![image](https://github.com/user-attachments/assets/249c83a8-5005-4faf-ab63-46e87f725819)

This solution is wrong, ideally we should get 111000 in all rows of ```latest_sales``` column.

![image](https://github.com/user-attachments/assets/79e31ba6-d7e2-4e9c-ae3b-d08b5f2502bc)

Let's look at explain plan.

We can see that the window here is ```unbounded preceeding and current row```

![image](https://github.com/user-attachments/assets/20a04927-9aeb-45bf-8458-9a8438ccfa9b)

What do these terms mean?

![image](https://github.com/user-attachments/assets/51dc44d0-ee2e-49ed-bcdf-2b0064e199fa)

- Unbounded preceeding : If i'm standing at a current row in a window I will return the result of any operation on the window from here to all the rows before me in the window.
- current_row : the row im standing at.
- Unbounded following : opposite of unbounded preceeding.
- rows_between(start_row,end_row) : basically the row we are currently at is 0, all rows before that are negative numbers and all rows after that is positive numbers.

![image](https://github.com/user-attachments/assets/ab7d0388-eff1-4780-835d-be88374a4807)

If we dont give anything then it just goes from current row to either unbounded preceeding (first row) of window or unbounded following (last row) of window.

Converting from string to unixtime when we have two fields date and time.

![image](https://github.com/user-attachments/assets/a1b00037-79e0-48be-b254-f8709e0c9616)

```emp_df = emp_df.withColumn("timestamp",from_unixtime(unix_timestamp(expr("CONCAT(date,' ',time)"),"dd-MM-yyyy HH:mm")))```

The timestamp column is a string.

![image](https://github.com/user-attachments/assets/b8767f27-92fc-4b03-bb70-2d1507ba368e)
