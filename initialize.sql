INSERT INTO user (first_name, last_name, username, password, billAddr)
VALUES ('John', 'Doe', 'JD',
        'scrypt:32768:8:1$lfyYhcjx0jtpGMdY$395bddf8e51f6fbbb6b58efb04623b4b7ef15a92ee14b2357e1b26419b94126887a13ff773069dd7c703405e33b210c4e5be0253eacf4ddd20a05de353e0089f',
        '114 NYU st'),
       ( 'Steven', 'Lu', 'SL'
       , 'scrypt:32768:8:1$lfyYhcjx0jtpGMdY$395bddf8e51f6fbbb6b58efb04623b4b7ef15a92ee14b2357e1b26419b94126887a13ff773069dd7c703405e33b210c4e5be0253eacf4ddd20a05de353e0089f'
       , '123 NYU st'),
       ('Peter', 'Juicy', 'PJ',
        'scrypt:32768:8:1$lfyYhcjx0jtpGMdY$395bddf8e51f6fbbb6b58efb04623b4b7ef15a92ee14b2357e1b26419b94126887a13ff773069dd7c703405e33b210c4e5be0253eacf4ddd20a05de353e0089f',
        '20 CU st'),
       ('Holy', 'Kai', 'HK',
        'scrypt:32768:8:1$lfyYhcjx0jtpGMdY$395bddf8e51f6fbbb6b58efb04623b4b7ef15a92ee14b2357e1b26419b94126887a13ff773069dd7c703405e33b210c4e5be0253eacf4ddd20a05de353e0089f',
        '20 CU st'),
       ('Denny', 'Zheng', 'DZ',
        'scrypt:32768:8:1$lfyYhcjx0jtpGMdY$395bddf8e51f6fbbb6b58efb04623b4b7ef15a92ee14b2357e1b26419b94126887a13ff773069dd7c703405e33b210c4e5be0253eacf4ddd20a05de353e0089f',
        '101 USC st');


INSERT INTO ServiceLocation (sLid, addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt) VALUES (1, '114 NYU st', '11201', '1A','2022-01-01',1000,2,3);
INSERT INTO ServiceLocation (sLid, addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt) VALUES (2, '123 NYU st', '11202', '6A','2022-08-15',760,1,2);
INSERT INTO ServiceLocation (sLid, addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt) VALUES (3, '211 NYU st', '11202', '11K','2022-08-17',1030,2,4);
INSERT INTO ServiceLocation (sLid, addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt) VALUES (4, '20 CU st', '10012', '3E','2022-07-22',670,1,1);
INSERT INTO ServiceLocation (sLid, addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt) VALUES (5, '20 CU st', '10012', '6C','2022-07-25',650,1,1);
INSERT INTO ServiceLocation (sLid, addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt) VALUES (6, '524 BROWN st', '53362', '2C','2022-08-16',980,2,2);
INSERT INTO ServiceLocation (sLid, addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt) VALUES (7, '196 UPENN st', '15213', '7C','2022-10-02',555,1,1);
INSERT INTO ServiceLocation (sLid, addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt) VALUES (8, '101 USC st', '52321', '16D','2022-08-16',1070,3,4);


INSERT INTO Customer_Service (cid, sLid) VALUES (1, 1);
INSERT INTO Customer_Service (cid, sLid) VALUES (2, 2);
INSERT INTO Customer_Service (cid, sLid) VALUES (2, 3);
INSERT INTO Customer_Service (cid, sLid) VALUES (3, 4);
INSERT INTO Customer_Service (cid, sLid) VALUES (4, 5);
INSERT INTO Customer_Service (cid, sLid) VALUES (4, 6);
INSERT INTO Customer_Service (cid, sLid) VALUES (5, 7);
INSERT INTO Customer_Service (cid, sLid) VALUES (5, 8);


INSERT INTO Model (modelid, modeltype, modelname, properties)
VALUES (1, "Light", "A Light 001", "An energy-efficient light meant to use in small house");
INSERT INTO Model (modelid, modeltype, modelname, properties)
VALUES (2, "Light", "A Light 002", "An energy-efficient light meant to use in medium-size house");
INSERT INTO Model (modelid, modeltype, modelname, properties)
VALUES (3, "Light", "A Light 003", "Great light to shine the whole room");
INSERT INTO Model (modelid, modeltype, modelname, properties)
VALUES (4, "Light", "A Light 004", "Unbelievable light to shine the whole room");
INSERT INTO Model (modelid, modeltype, modelname, properties)
VALUES (5, "Refrigerator", "B Refrigerator 01", "Basic refrigerator");
INSERT INTO Model (modelid, modeltype, modelname, properties)
VALUES (6, "Refrigerator", "B Refrigerator 02", "Advanced refrigerator");
INSERT INTO Model (modelid, modeltype, modelname, properties)
VALUES (7, "Refrigerator", "B Refrigerator 03", "Deluxe refrigerator");
INSERT INTO Model (modelid, modeltype, modelname, properties)
VALUES (8, "Air-Conditioner", "C Air Conditioner 01", "basic air conditioner but energy-efficient");
INSERT INTO Model (modelid, modeltype, modelname, properties)
VALUES (9, "Air-Conditioner", "C Air Conditioner 02", "best air conditioner");

INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (1,"light",1,1);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (2,"light",2,1);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (3,"light",3,1);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (4,"light",1,1);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (5,"refrigerator",6,1);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (6,"AC system",9,1);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (7,"light",4,2);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (8,"light",4,2);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (9,"refrigerator",5,2);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (10,"AC system",8,2);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (11,"light",1,3);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (12,"light",2,3);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (13,"light",4,3);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (15,"refrigerator",7,3);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (16,"AC system",8,3);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (17,"AC system",9,3);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (18,"light",1,4);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (19,"light",2,4);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (20,"refrigerator",5,4);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (21,"AC system",8,4);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (22,"light",1,5);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (23,"light",2,5);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (24,"refrigerator",5,5);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (25,"AC system",8,5);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (26,"light",1,6);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (27,"light",1,6);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (28,"light",2,6);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (29,"refrigerator",6,6);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (30,"AC system",9,6);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (31,"light",1,7);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (32,"light",1,7);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (33,"refrigerator",5,7);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (34,"AC system",8,7);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (35,"light",2,8);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (36,"light",2,8);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (37,"light",3,8);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (38,"light",4,8);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (39,"refrigerator",7,8);
INSERT INTO Device(deviceid,type,modelid,SLid) VALUES (40,"AC system",9,8);


INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (1,1,'2023-08-01 10:30:00',"switched on",NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (2,1,'2023-08-01 10:35:00',"energy use", 0.16);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (3,1,'2023-08-01 10:40:00',"energy use", 0.15);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (4,1,'2023-08-01 10:40:00',"switched off", NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (5,5,'2023-08-01 10:40:00',"door opened", NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (6,5,'2023-08-01 11:15:00',"door closed", NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (7,5,'2023-08-01 11:15:00',"energy use", 5.62);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (8,6,'2023-08-01 10:00:00',"energy use", 6.4);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (9,3,'2023-08-02 14:00:00',"energy use", 0.33);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (10,9,'2023-09-13 21:40:00',"door opened", NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (11,9,'2023-09-13 22:05:00',"door closed", NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (12,9,'2023-09-13 22:05:00',"energy use", 5.83);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (13,9,'2023-11-25 10:00:00',"energy use", 1.83);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (14,8,'2023-11-25 11:00:00',"energy use", 0.16);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (15,31,'2023-11-25 11:00:00',"energy use", 0.26);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (16,13,'2023-11-25 16:00:00',"energy use", 0.19);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (17,1,'2022-08-21 10:35:00',"energy use", 0.18);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (18,1,'2022-08-01 10:40:00',"energy use", 0.11);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (19,5,'2022-08-01 11:15:00',"energy use", 3.62);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (20,6,'2022-08-01 10:00:00',"energy use", 6.75);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (21,3,'2022-08-02 14:00:00',"energy use", 0.63);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (22,9,'2023-10-13 1:40:00',"door opened", NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (23,9,'2023-10-13 1:45:00',"door closed", NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (24,9,'2023-10-13 2:40:00',"door opened", NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (25,9,'2023-10-13 2:55:00',"door closed", NULL);
INSERT INTO Datas (dataid, deviceid,timestamp,eventLabel,value) VALUES (26,40,'2022-08-17 14:00:00',"energy use", 11.63);
INSERT INTO Datas (deviceid,timestamp,eventLabel,value) VALUES (31,'2023-12-10 11:00:00',"energy use", 0.36);
INSERT INTO Datas (deviceid,timestamp,eventLabel,value) VALUES (33,'2023-12-08 11:00:00',"energy use", 5.36);
INSERT INTO Datas (deviceid,timestamp,eventLabel,value) VALUES (32,'2023-12-08 12:00:00',"energy use", 1.15);
INSERT INTO Datas (deviceid,timestamp,eventLabel,value) VALUES (40,'2023-12-09 17:00:00',"energy use", 11.14);
INSERT INTO Datas (deviceid,timestamp,eventLabel,value) VALUES (30,'2023-12-10 10:00:00',"energy use", 14.53);


INSERT INTO Price (fromtime, endtime, zipcode, price)
VALUES ('00:00:00', '07:00:00', 11201, 1.62),
       ('07:00:01', '12:00:00', 11201, 2.14),
       ('12:00:01', '18:00:00', 11201, 3.65),
       ('18:00:01', '22:00:00', 11201, 1.98),
       ('22:00:01', '23:59:59', 11201, 1.83),
       ('00:00:00', '07:00:00', 11111, 1.63),
       ('07:00:01', '12:00:00', 11111, 2.15),
       ('12:00:01', '18:00:00', 11111, 3.67),
       ('18:00:01', '22:00:00', 11111, 2.06),
       ('22:00:01', '23:59:59', 11111, 1.77),
       ('00:00:00', '07:00:00', 15213, 1.33),
       ('07:00:01', '12:00:00', 15213, 1.87),
       ('12:00:01', '18:00:00', 15213, 3.34),
       ('18:00:01', '22:00:00', 15213, 1.72),
       ('22:00:01', '23:59:59', 15213, 1.53),
       ('00:00:00', '07:00:00', 52321, 2.34),
       ('07:00:01', '12:00:00', 52321, 2.64),
       ('12:00:01', '18:00:00', 52321, 4.52),
       ('18:00:01', '22:00:00', 52321, 2.52),
       ('22:00:01', '23:59:59', 52321, 2.01);