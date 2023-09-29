SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `sbrp` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `sbrp`;


DROP TABLE IF EXISTS `access_rights`;
CREATE TABLE IF NOT EXISTS `access_rights`(
    `Access_right_no` int NOT NULL,
    `role` varchar(20) NOT NULL,
    CONSTRAINT access_rights_pk PRIMARY KEY (Access_right_no)
);

CREATE TABLE IF NOT EXISTS `Staff` (
    `Staff_ID` int NOT NULL,
    `Staff_FName` varchar(50) NOT NULL,
    `Staff_LName` varchar(50) NOT NULL,
    `Dept` varchar(50) NOT NULL,
    `Country` varchar(50) NOT NULL,
    `Email` varchar(50) NOT NULL,
    `Access_Rights` int NOT NULL,
    CONSTRAINT staff_pk PRIMARY KEY (Staff_ID),
    CONSTRAINT staff_fk FOREIGN KEY (Access_Rights) REFERENCES access_rights(Access_right_no) 
);

CREATE TABLE IF NOT EXISTS `role` (
    `role_name` varchar(20) NOT NULL,
    `role_descr` longtext NOT NULL,
    CONSTRAINT role_pkey PRIMARY KEY (role_name)
);

CREATE TABLE IF NOT EXISTS `Role_Skill`(
    `Role_Name` varchar(20),
    `Skill_Name` varchar(50),
    CONSTRAINT Role_skill_pk PRIMARY KEY (Role_Name, Skill_Name),
    CONSTRAINT role_skill_fk1 FOREIGN KEY (Role_Name) REFERENCES role(role_name),
    CONSTRAINT role_skill_fk2 FOREIGN KEY (Skill_Name) REFERENCES skills(Skill_Name) 
);

CREATE TABLE IF NOT EXISTS `skills`(
    `Skill_Name` varchar(50) NOT NULL,
    CONSTRAINT skills_pk PRIMARY KEY (Skill_Name)
)

CREATE TABLE IF NOT EXISTS `Staff_Skill` (
    `Staff_ID` int NOT NULL,
    `Skill_Name` varchar(50) NOT NULL,
    CONSTRAINT Staff_skill_pk PRIMARY KEY (Staff_ID, Skill_Name),
    CONSTRAINT Staff_skill_fk1 FOREIGN KEY (Skill_Name) REFERENCES skills(Skill_Name),
    CONSTRAINT Staff_skill_fk2 FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID) 
);

