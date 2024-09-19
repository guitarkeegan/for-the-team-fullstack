# Clippers Take Home Project

## Quick Start

## Loading data

You can replace the backend/dev_test_data folder with new files. As long
as they share the same names, they should be loaded into the database just fine.

## Questionare 

I have links throughout the form to the api routes. If you have the backend running
you will see the json outputs.

### Backend
1. Start the backend services using Docker Compose:
   ```
   docker compose --profile backend build
   docker compose --profile backend up
   ```

### Frontend
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Run the Next.js development server:
   ```
   npm run dev
   ```

Access the application at `http://localhost:3000`
Access the api through curl or browser at `http://localhost:5000`


## Notes
- The backend should be running before starting the frontend.
- I was unable to dockerize the next JS application so please try running it locally.

I also made a quick video of the front end
(Front End)[https://www.loom.com/share/71064cb072eb4e908b2d7b0637fceea0?sid=f3daa7c2-d20e-45c0-acaa-1272e50f5d54]
