# Align Coaching Web App (Frontend)

## Project Overview

The Align Coaching Web App frontend is a single-page application built with **React** and **Vite**. It provides the user interface for the Align Coaching platform, allowing coaches and clients to interact with the system via a fast and responsive web UI. This project uses **Tailwind CSS** for styling, **React Router** for client-side routing, **Axios** for API calls, and **React-Toastify** for notifications. The source code is organized in the `src` directory, and an import alias `@` is configured (pointing to `src/`) to simplify module imports. The app is configured to be deployed as a static site for production.

## Getting Started (Installation & Development)

**Prerequisites:** Make sure you have **Node.js v18+** and npm installed on your system.

To set up the development environment and run the app locally, follow these steps:

1. **Clone the repository:** If you haven't already, clone the Align Coaching frontend repository to your local machine.
2. **Install dependencies:** In the project root directory, run `npm install` to install all required packages.
3. **Start the development server:** Run `npm run dev`. This will start Vite's development server and compile the app. By default, the app will be available at **http://localhost:5173/**. Open this URL in your browser to view the application. (The development server supports hot-reloading, so any code changes will automatically refresh the app in the browser.)
4. **Explore the app:** You can now navigate through the application’s pages and features. React Router is used for navigation, so you can use the app without full page reloads as you move between views.

## Environment Setup

If the application requires environment-specific variables (for example, API endpoints or keys), you should configure them before running the app or building for production:

- **Creating a .env file:** In the project root, create a file named **.env** (this file is ignored by Git). Define any needed variables in this file. For example, to set an API base URL, you might add a line like:<br>
  ```text
  VITE_API_URL=https://api.aligncoaching.com
