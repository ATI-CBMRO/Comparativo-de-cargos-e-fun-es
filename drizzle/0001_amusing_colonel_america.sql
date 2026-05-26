CREATE TABLE `operational_commands` (
	`id` int AUTO_INCREMENT NOT NULL,
	`stateId` int NOT NULL,
	`nomenclature` varchar(300) NOT NULL,
	`acronym` varchar(50),
	`subdivisions` text,
	`attributions` text,
	`detailLevel` enum('detalhado','moderado','basico') NOT NULL,
	`legalBasis` varchar(300),
	`notes` text,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `operational_commands_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `states` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(100) NOT NULL,
	`sigla` varchar(2) NOT NULL,
	`region` enum('Norte','Nordeste','Centro-Oeste','Sudeste','Sul') NOT NULL,
	`corporationName` varchar(200) NOT NULL,
	`legislationDocuments` text,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `states_id` PRIMARY KEY(`id`),
	CONSTRAINT `states_sigla_unique` UNIQUE(`sigla`)
);
--> statement-breakpoint
CREATE TABLE `technical_directorates` (
	`id` int AUTO_INCREMENT NOT NULL,
	`stateId` int NOT NULL,
	`nomenclature` varchar(300) NOT NULL,
	`acronym` varchar(50),
	`subdivisions` text,
	`attributions` text,
	`detailLevel` enum('detalhado','moderado','basico') NOT NULL,
	`legalBasis` varchar(300),
	`notes` text,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `technical_directorates_id` PRIMARY KEY(`id`)
);
