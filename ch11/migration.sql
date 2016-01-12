-- Running upgrade 34044511331 -> 2e6a6cc63e9

ALTER TABLE cookies RENAME TO new_cookies;

UPDATE alembic_version SET version_num='2e6a6cc63e9' WHERE alembic_version.version_num = '34044511331';

