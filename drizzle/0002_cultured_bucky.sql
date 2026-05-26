CREATE TABLE `positions` (
	`id` int AUTO_INCREMENT NOT NULL,
	`operationalCommandId` int,
	`technicalDirectorateId` int,
	`title` varchar(200) NOT NULL,
	`acronym` varchar(50),
	`rank` varchar(100),
	`subordinateTo` varchar(200),
	`subordinates` text,
	`attributions` text,
	`sortOrder` int DEFAULT 0,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `positions_id` PRIMARY KEY(`id`)
);
