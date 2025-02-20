# Описание ORM моделей

## 1. Модель `File`
### Описание:
Модель `File` представляет собой сущность файла, хранящегося в БД. 
Файл может быть загружен пользователем и храниться в локальном или удалённом хранилище S3.

### Поля:
- **file_id** *(int, primary key, autoincrement, not null)* — Идентификатор файла в базе данных.
- **file_key** *(string, unique, not null)* — Ключ файла в формате `{file_path}/{file_name}`, используется для идентификации файлов в S3.
- **mime_type** *(`AllowedFileFormats`, not null, default=`INCORRECT_FILE_FORMAT`)* — MIME-тип файла.
- **status** *(`FileStatus`, nullable, default=`ACTIVE`)* — Статус файла (можно ли получить по S3 ссылке 
или хранится ли локально).
- **bucket_name** *(string, nullable)* — Название бакета S3, если файл загружен в облачное хранилище.
- **s3_url** *(string, nullable)* — Прямая ссылка на файл в S3.
- **expires_at** *(datetime, nullable)* — Время истечения срока действия ссылки на файл.
- **uploaded_at** *(datetime, not null, default=datetime.now())* — Время загрузки файла на сервер.
- **added_user** *(int, nullable, ForeignKey(users.user_id))* — Идентификатор пользователя, загрузившего файл.

### Связи:
- **users** — Пользователь, который добавил файл.

### Дополнительно:
- `file_key` должен быть уникальным.

## 2. Модель `UserDetails`
### Описание:
Модель `UserDetails` хранит дополнительную информацию о пользователе.

### Поля:
- **user_id** *(int, primary key, ForeignKey(users.user_id), not null)* — Идентификатор пользователя.
- **description** *(Text, nullable)* — Описание профиля пользователя.
- **profile_image_id** *(int, nullable, ForeignKey(files.file_id))* — Идентификатор файла аватарки пользователя.

### Связи:
- **users** — Для каждого пользователя, может быть только одна сущность описывающая его дополнительную информацию.
- **files** — Изображение аватарки пользователя (Может быть только одно у каждого пользователя).

## 3. Модель `UserCredentials`
### Описание:
Модель `UserCredentials` хранит данные для аутентификации пользователя.

### Поля:
- **user_id** *(int, primary key, ForeignKey(users.user_id), not null)* — Идентификатор пользователя.
- **email** *(string, unique, not null)* — Email пользователя.
- **password_hash** *(string, not null)* — Хеш пароля пользователя.
- **password_encryption** *(`PasswordEncryptionTypes`, not null, default=`NONE`)* — Метод шифрования пароля.

### Связи:
- **users** — У одного пользователя, может быть только одна сущность для хранения его аутентификационных данных.

## 4. Модель `User`
### Описание:
Модель `User` представляет собой пользователя системы.

### Поля:
- **user_id** *(int, primary key, autoincrement, not null)* — Идентификатор пользователя.
- **username** *(string, unique, not null)* — Никнейм пользователя.
- **role** *(`UserRoleDB`, not null, default=`USER`)* — Роль пользователя в системе (например, обычный пользователь, администратор и т. д.).
- **created_at** *(datetime, not null, default=datetime.now())* — Дата регистрации пользователя.

### Дополнительно:
TODO: добавить связи с 
- `support_request`
- `user_personal_list`
- `book_rating`
- `user_bookmark`
- `books`
- `author_curators`
- `publisher_curators`