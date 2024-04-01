UPDATE full_names
SET status = (SELECT status FROM short_names WHERE SUBSTRING_INDEX(full_names.name, '.', 1) = short_names.name);



-- Создание индекса для таблицы full_names
CREATE INDEX idx_name_full_names ON full_names(name);
-- Создание индекса для таблицы short_names
CREATE INDEX idx_name_short_names ON short_names(name);

UPDATE full_name
JOIN short_name ON SUBSTRING_INDEX(full_name.name, '.', 1) = short_name.name
SET full_name.status = short_name.status;



UPDATE full_names
SET status = (SELECT short_names.status
              FROM short_names
              WHERE SUBSTRING_INDEX(full_names.name, '.', 1) = short_names.name)
WHERE EXISTS (
    SELECT 1
    FROM short_names
    WHERE SUBSTRING_INDEX(full_names.name, '.', 1) = short_names.name
);



-- Создание временной таблицы для хранения соответствия имен файлов без расширения и с расширением
CREATE TEMPORARY TABLE file_names_mapping (
    file_name_without_extension VARCHAR(255),
    file_name_with_extension VARCHAR(255)
);
-- Заполнение временной таблицы данными
INSERT INTO file_names_mapping (file_name_without_extension, file_name_with_extension)
SELECT
    SUBSTRING_INDEX(full_names.name, '.', 1),
    full_names.name
FROM
    full_names;
-- Обновление статуса в таблице full_names с использованием временной таблицы
UPDATE full_names
JOIN short_names ON file_names_mapping.file_name_with_extension = short_names.name
SET full_names.status = short_names.status
WHERE file_names_mapping.file_name_without_extension = short_names.name
