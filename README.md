# Subscene data to Telegram Importer

## Database Configuration

You need to add a new column named `tg_post_id` to subscene database table. This column should be of type `INT` and better be `unique`. This column will be used to store the Telegram post id of the subtitle for later usages.

```sql
ALTER TABLE `all_subs` ADD `tg_post_id` INT UNIQUE;
```