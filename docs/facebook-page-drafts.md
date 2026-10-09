# Facebook Page draft integration

## Supported target

This integration targets a Facebook **Page** through Meta's Graph API. It does not target a personal profile or a Facebook Group.

Meta's Page Feed endpoint is `POST /{page-id}/feed`. The request sets `published=false`, so the client creates an unpublished Page post and does not publish it.

## Required configuration

The process reads these environment variables:

- `META_PAGE_ID` — the Page identifier.
- `META_PAGE_ACCESS_TOKEN` — a Page access token. It is sent in the HTTP `Authorization` header and is never written to repository files.
- `META_GRAPH_VERSION` — optional Graph API version. The default is `v26.0`, matching the current Meta Pages API documentation used for this integration.

The token must be issued through Meta user authentication for a person with the required Page task. Meta documents these permissions for Page posting:

- `pages_show_list`
- `pages_read_engagement`
- `pages_manage_posts`

Meta may require App Review for extended permissions. The app owner must complete Meta's own authentication, review, and Page authorization process.

## Functional commands

`create-draft` sends a message and optional link to the Page Feed endpoint with `published=false`.

`list-drafts` requests unpublished items from the Page Feed endpoint and asks for `id`, `message`, and `created_time`.

There is no publish command in this client. Publication requires a separate, deliberate workflow outside this draft-only integration.

## Official documentation

- [Meta Facebook Pages API](https://developers.facebook.com/documentation/pages-api)
- [Meta Page Feed Graph API reference](https://developers.facebook.com/docs/graph-api/reference/page/feed/)
- [Meta permissions reference](https://developers.facebook.com/documentation/development/permissions)
