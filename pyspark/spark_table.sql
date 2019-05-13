USE sklearn_data;


DROP TABLE IF EXISTS spark_data;
DROP TABLE IF EXISTS Rec;
DROP TABLE IF EXISTS demo2_data_prediction;

CREATE TABLE IF NOT EXISTS spark_data
(
  cust_id varchar(255),
  age int,
  job varchar(255),
  marital varchar(255),
  education varchar(255),
  defaulters varchar(255),
  balance int,
  housing varchar(255),
  loan varchar(255),
  contact varchar(255),
  day varchar(255),
  month varchar(255),
  duration int,
  campaign int,
  pdays int,
 previous int,
poutcome varchar(255),
deposit varchar(255),
PRIMARY KEY (cust_id)
);


CREATE TABLE IF NOT EXISTS Rec
(
  cust_id varchar(255),
  age int,
  job varchar(255),
  marital varchar(255),
  education varchar(255),
  defaulters varchar(255),
  balance int,
  housing varchar(255),
  loan varchar(255),
  contact varchar(255),
  day varchar(255),
  month varchar(255),
  duration int,
  campaign int,
  pdays int,
 previous int,
poutcome varchar(255),
deposit varchar(255),
job_indexed int,
marital_indexed int,
education_indexed int,
PRIMARY KEY (cust_id)
);

CREATE TABLE IF NOT EXISTS demo2_data_prediction
(
  age int,
  duration int,
  campaign int,
  pdays int,
  previous int,
  poutcome varchar(255),
  deposit varchar(255),
  job_indexed int,
  marital_indexed int,
  education_indexed int,
  job varchar(255),
  marital varchar(255),
  education varchar(255),
  defaulters varchar(255),
  balance int,
  housing varchar(255),
  loan varchar(255),
  contact varchar(255),
  predict_class int
);


