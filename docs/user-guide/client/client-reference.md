# Client
Geocube-client has three level of access:

- `Client` is for basic access. The `Client` has [CRUD](https://fr.wikipedia.org/wiki/CRUD) access to most entities. It can also index new images.
- [Consolidater](consolidater-reference.md) is for optimization of the database, through consolidation of the datasets. It has CRUD access to `entities.job`.
- [Admin](admin-reference.md) is for operation that must be done wisely and cautiously.

::: geocube.Client
