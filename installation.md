# POSN-CMS Development Environment Setup

This document outlines the complete steps to deploy and configure the development Docker environment for POSN-CMS.

---

## 1. Prerequisites

Before you begin, ensure you have the following installed on your system:
* **[Docker](https://docs.docker.com/get-docker/)** (recent version)
* **[Docker Compose](https://docs.docker.com/compose/install/)**

## 2. Start the Development Container

Open a terminal in the root of the `POSN-CMS` repository and execute the provided development script:

```bash
./cms-dev.sh
```

> **Note for Windows Users:** > If you cannot run the `.sh` script, you can execute the equivalent Docker Compose command directly:
> ```bash
> docker compose -p posn-cms-dev -f docker-compose.dev.yml run --build --rm --service-ports devcms
> ```

This process will build the CMS image (if necessary) and drop you into a `bash` shell **inside** the container.

Your local source code is automatically mounted inside the container at `/home/cmsuser/cms`. Any code changes you make on your host machine will be immediately reflected inside the container.

## 3. Initialize the Database

The first time you run the development container, the database will be empty. From inside the container's bash prompt, run the following commands to create and initialize it:

```bash
# Create the PostgreSQL database
createdb -h devdb -U postgres cmsdb

# Initialize the CMS database schema
cmsInitDB
```

## 4. Import Test Data (Optional but Recommended)

To properly test the platform, it is highly recommended to load a sample contest. You can clone the CMS test repository and import it directly from the container shell:

```bash
git clone [https://github.com/cms-dev/con_test.git](https://github.com/cms-dev/con_test.git)
cd con_test

# Import the test users
cmsImportUser --all

# Import the contest data
cmsImportContest -i .
```

## 5. Start the Servers

With the database initialized and populated, you can now start the CMS servers. For example, to launch the Contest Web Server, run:

```bash
cmsContestWebServer
```

> **Tip:** If the system prompts you to choose a contest ID, you can simply press **Enter**.

## 6. Access the Application

Once the server is running, the ports are forwarded to your host machine. You can access the CMS web interfaces from your standard web browser:

* **Contest Web Server:** [http://localhost:8888/](https://www.google.com/search?q=http://localhost:8888/)
* **Admin Web Server** *(if started)*: [http://localhost:8889/](https://www.google.com/search?q=http://localhost:8889/)

---

## Notes for Future Development

* **Applying Code Changes:** Since your local repository is mounted, you can edit the Python code directly on your host machine. If you change core components, you can apply them inside the container by running `pip3 install . --break-system-packages` without needing to rebuild the entire Docker image.
* **Data Persistence:** The database data is saved to a `.dev/postgres-data` directory on your host machine. If you exit the container and run `./cms-dev.sh` again later, your database state and imported contests will be safely preserved.
