# Additional Questions - Architecture & Design

## Question 1: Do you think this is a good architecture with a scalable design?

Yes, I think the architecture is well-structured and works nicely for a multi-tenant organization management system. One of the biggest strengths is the data isolation — each organization gets its own MongoDB collection, which keeps their data completely separate. This improves security and makes it easier to manage each tenant independently. Also, since collections are created dynamically, adding a new organization doesn’t affect the existing ones.

I also feel the code is organized in a clean way. The routes handle API calls, services contain the logic, and utilities take care of common functions like JWT and hashing. This separation makes the project easier to maintain and extend.

From a scalability point of view, MongoDB’s horizontal scaling helps as the number of organizations grows, and using JWT tokens keeps the API stateless, which is helpful if we add more backend instances later.

But there are some limitations too. If the system grows to thousands of organizations, having too many collections might eventually slow things down because MongoDB still needs to manage metadata for each one. Also, the master database holding all organization metadata could become a bottleneck at very large scale.

Overall, I think this architecture is solid for small to medium-sized deployments and provides a good base that can be improved later.


## Question 2: What can be the trade-offs with the tech stack and design choices?

There are a few important trade-offs with the choices I made in this project.

**FastAPI vs Django/Flask:** FastAPI is really fast and modern, and the auto-generated docs are super helpful. But compared to Django, it has fewer built-in features and a smaller ecosystem. So I had to implement things manually that Django would have handled for me.

**MongoDB vs SQL:** MongoDB fits well because it’s flexible and doesn’t force strict schemas, which works nicely when different organizations may need slightly different fields. However, the downside is losing SQL features like joins and foreign keys. That means I have to enforce data integrity in the application instead of relying on the database.

**Collection-per-organization design:** This gives excellent data isolation, but it also means cross-organization queries are harder. Also, schema updates need to be applied to every collection individually, which can become tedious. MongoDB also isn’t optimized for extremely large numbers of collections.

**JWT Authentication:** JWTs make the backend stateless, which is great for scaling horizontally. But token revocation becomes harder — if a user gets removed, their old token will still work until it expires. To fix this, I would need a blacklist system or shorter token lifetimes.

**Sync vs Async DB operations:** Since I used pymongo (which is synchronous), I’m not fully using FastAPI’s async capabilities. This could limit the number of concurrent requests the server can handle. But on the positive side, synchronous code is easier to understand.

**Master Database:** Having all org metadata in one place is convenient, but it becomes a single point of failure. If that database goes down, the entire system is affected.


## Question 3: Briefly explain if you can design something better.

If I get the chance to improve the design, there are a few things I would focus on:

**Adding caching (Redis):** Frequently accessed data like organization metadata could be cached to make responses faster and reduce load on the main database.

**Using async DB operations:** Switching from pymongo to motor would allow the backend to handle more concurrent requests since FastAPI is designed for async operations.

**Hybrid multi-tenancy:** Instead of creating a collection for every single organization, I could use a mix — smaller organizations could share a collection with an organization_id field, and only larger ones get their own collection. This prevents hitting MongoDB’s collection-count limits.

**Improved token system:** Adding refresh tokens and a blacklist would help control login sessions and make invalidation easier.

**Add monitoring and metrics:** Logging, health checks, and metrics would make it easier to debug issues and track performance in production.

**Connection pooling and rate limiting:** These would improve performance and also protect the system against brute-force attacks.

If the system eventually grows extremely large (like 10k+ tenants), I might even consider sharding or splitting the application into microservices. But for now, the current design is a strong starting point, and these improvements can be added gradually as the requirements grow.
