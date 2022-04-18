CREATE TABLE `Entry` (
        `id` INTEGER NOT NULL PRIMARY KEY,
        `concept` TEXT NOT NULL,
        `entry` TEXT NOT NULL,
        `mood_id` INTEGER NOT NULL,
        `date` TEXT NOT NULL,
        FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
        `id` INTEGER NOT NULL PRIMARY KEY,
        `label` TEXT NOT NULL
);

INSERT INTO `Mood` VALUES (null, 'Happy');
INSERT INTO `Mood` VALUES (null, 'Sad');
INSERT INTO `Mood` VALUES (null, 'Angry');
INSERT INTO `Mood` VALUES (null, 'Ok');

INSERT INTO `Entry` VALUES (null, 'Javascript', 'I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.', 1, 'Wed Sep 15 2021 10:10:47');
INSERT INTO `Entry` VALUES (null, 'Python', 'Python is named after the Monty Python comedy group from the UK. I am sad because I thought it was named after the snake', 4, 'Wed Sep 15 2021 10:11:33');
INSERT INTO `Entry` VALUES (null, 'Python', 'Why did it take so long for python to have a switch statement? It is much cleaner than if/elif blocks', 3, 'Wed Sep 15 2021 10:13:11');
INSERT INTO `Entry` VALUES (null, 'Javascropt', 'Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.', 3, 'Wed Sep 15 2021 10:14:05');