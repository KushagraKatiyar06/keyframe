# KeyFrame Frontend

---

## 1. Prereqs

| Action | Command | Notes |
| :--- | :--- | :--- |
| **Prerequisite** | Install Node.js (v18+ recommended) | Ensures compatibility. |
| **Setup** | `npm install` | Installs Next.js and required packages (`uuid`). |
| **Run** | `npm run dev` | Starts the local server at **`http://localhost:3000`**. |

---

## 2. Setup & Static Assets (CRITICAL)

Before running the app, you must place the following static files in the specified location for the design and mock API to function: Will still work if you don't.

| File Type | Required Location | Purpose |
| :--- | :--- | :--- |
| **Logo** | `public/assets/Logo_Transparent.png` | Used by the Navbar and Home Page UI. |
| **Mock Video** | `public/assets/videos/mock.mp4` | Simulates the final video output for the completion state. |
| **Mock Thumbnail**| `public/assets/thumbnails/mock.jpg` | Used as the video poster for the mock output. |

---

## 3. Project File Structure & Overview

The project uses the **Next.js App Router** convention: **Folders define routes**, and the **`page.tsx` file defines the UI** for that route. All styling is done using **CSS Modules**.

### UI Pages (Frontend)

| Route Path | File Location | Brief Overview |
| :--- | :--- | :--- |
| **`/`** | `src/app/page.tsx` | The **Home Page**. Contains the Splash Screen, the Prompt Form, and initiates the job submission. |
| **`/status/[jobId]`** | `src/app/status/[jobId]/page.tsx` | The **Status/Waiting Page**. Handles continuous polling of the mock API, displays progress, and shows the mock video upon completion. |
| **`/feed`** | `src/app/feed/page.tsx` | **Placeholder** page for the Community Videos feed. |
| **`/team`** | `src/app/team/page.tsx` | **Placeholder** page for team information. |

### API Mock Handlers (Local Backend)

These files simulate the Node.js API Gateway and are essential for local development testing.

| API Endpoint | File Location | Role |
| :--- | :--- | :--- |
| **`/api/v1/generate`** | `src/app/api/v1/generate/route.js` | Receives the prompt and instantly returns a mock `jobId` (`HTTP 202`). |
| **`/api/v1/status/[id]`** | `src/app/api/v1/status/[jobId]/route.js` | Cycles through **QUEUED** → **PROCESSING** → **COMPLETE** statuses to simulate job progress. |
| **`/api/v1/feed`** | `src/app/api/v1/feed/route.js` | Returns mock data for the "While You Wait" Community Feed. |

---

## 4. Quality & Collaboration

### Linting (Before Pull Request)

**Always run linting** before submitting a Pull Request to ensure code quality and consistency.

| Action | Command |
| :--- | :--- |
| **Lint Check** | `npm run lint` |
| **Lint Fix** | `npm run lint -- --fix` |