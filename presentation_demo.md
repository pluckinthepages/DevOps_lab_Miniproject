# CampusFind – Step-by-Step Demo Guide

This guide walks you through CampusFind one click at a time. You do not need to know programming. Follow each step in order and do not skip any.

**What is CampusFind?** It is a website for a college campus. If you **lose** something (keys, a bottle, headphones), you post it on the website. If you **find** something that isn't yours, you post that too. Everyone can search the list, and the person who posted an item can mark it as returned.

**How to read this guide:**
- Text in **bold** is exactly what you will see on the screen: a button, a link or a heading.
- Text in `grey boxes` is exactly what you type. Copy it letter for letter.
- ✅ **You should see:** tells you what the screen should look like after a step. If your screen looks different, go back one step and try again.

---

## Part 1 – Start the app (one time, about 2 minutes)

The app needs to be started once before you can use it in the browser. This is the only part that uses typed commands. After this, everything is done with the mouse.

### Step 1.1 – Open the Terminal app
1. On your Mac keyboard, press and hold the **Command (⌘)** key, then press the **Space bar**. A search bar appears in the middle of the screen.
2. Type `Terminal`.
3. Press the **Return** key.

✅ **You should see:** a window with a white or black background and a blinking cursor.

### Step 1.2 – Go to the project folder
1. In the Terminal window, type `cd` followed by **one space**. Do **not** press Return yet.
2. Open **Finder** and find the project folder named **DevOps_lab_Miniproject**.
3. **Drag that folder** with your mouse and drop it into the Terminal window. The folder's location appears after `cd `.
4. Now press **Return**.

✅ **You should see:** the Terminal line now ends with `DevOps_lab_Miniproject`.

### Step 1.3 – Start the website
Copy the line below exactly, paste it into Terminal (**⌘ + V**), and press **Return**.

**If this is the first time on this computer**, use this line:

```
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python scripts/seed_demo_data.py && PORT=8000 FLASK_ENV=development python app.py
```

**If you have done this before on this computer**, use this shorter line:

```
source .venv/bin/activate && python scripts/seed_demo_data.py && PORT=8000 FLASK_ENV=development python app.py
```

✅ **You should see:** a few lines of text ending with `Running on http://127.0.0.1:8000`. The command line does **not** come back. That is normal: it means the website is running.

> ⚠️ **Keep this Terminal window open** for the whole demo. Closing it switches the website off. You can minimise it with the yellow button in the top-left corner.

> ℹ️ The website uses port **8000** and not 5000. On Macs, port 5000 is often used by the AirPlay feature.

### Step 1.4 – Open the website
1. Open **Google Chrome** or **Safari**.
2. Click the address bar at the very top of the browser window.
3. Type `localhost:8000` and press **Return**.

✅ **You should see:** a page with **CampusFind** in the top-left corner and a large heading **CampusFind** below it.

---

## Part 2 – Look around without logging in

### Step 2.1 – Read the four number boxes
Below the heading are four white boxes with numbers:

| Box | What it means | Number you should see |
|---|---|---|
| **Total reports** | Every item ever posted | **12** |
| **Lost** | Items people have lost | **6** |
| **Found** | Items people have found | **6** |
| **Resolved** | Items returned to their owner | **2** |

These numbers update automatically every time an item is added, changed or deleted.

### Step 2.2 – Look at the item cards
1. Scroll down with your mouse or trackpad.
2. You will see a grid of cards. Each card is one item.
3. Each card has two coloured labels at the top:
   - **LOST** in red, or **FOUND** in teal (blue-green).
   - **OPEN** in orange (still missing), **CLAIMED** in blue (someone has said it is theirs) or **RESOLVED** in green (returned).
4. At the bottom of each card you will see where the item was lost or found, and on what date.

### Step 2.3 – Go to page 2
1. Scroll to the very bottom of the page.
2. You will see **Page 1 of 2**. Click **Next →**.

✅ **You should see:** 3 more cards. Click **← Previous** to go back.

### Step 2.4 – Search for an item
1. Scroll back to the top.
2. Click the long white box that says **Search title, description or location…**
3. Type `headphones`.
4. Click the purple **Search** button.

✅ **You should see:** **1 result found** and a single card: **Sony WH-1000XM4 Headphones near Cafeteria**.

### Step 2.5 – Use the filters
1. Click the **Clear** button to remove the search.
2. Click the **Filters** button (to the right of **Search**). Three drop-down menus appear.
3. Click the first menu (**All categories**) and choose **Keys**. The page updates by itself; you do not need to press anything.

   ✅ **You should see:** 2 results: **Dorm Room Keys on Red Lanyard** and **Silver Bike Lock Key**.

4. Click **Clear**. Then click **Filters** again, open the third menu (**Any status**) and choose **Resolved**.

   ✅ **You should see:** 2 green **RESOLVED** items. This is the same number as the **Resolved** box at the top.

5. Click **Clear** to show all items again.

### Step 2.6 – Open one item
1. Click anywhere on the card **Sony WH-1000XM4 Headphones near Cafeteria**.

✅ **You should see:** a full page about the item showing its **Location**, the **Date found**, who **Reported by** it (**priya.s**) and a **Contact** email address. There is a purple button **Contact finder**. Clicking it opens your email app with a message already addressed to the finder.

2. Click **← Back to board** at the top to return.

### Step 2.7 – Try to post without logging in
1. Click the purple **Report an item** button near the top of the home page.

✅ **You should see:** the **Welcome back** login page, with an orange message: **Please log in to continue.** Only logged-in users can post. This protects the board from anonymous spam.

---

## Part 3 – Log in and post an item

### Step 3.1 – Log in with the demo account
On the **Welcome back** page:
1. Click the **Email or username** box and type `demo@campus.edu`
2. Click the **Password** box and type `DemoPassword123!` (capital D, capital P, and an exclamation mark at the end).
3. Click the purple **Log in** button.

✅ **You should see:** a green message **Logged in as demo.** The **Report an item** page opens automatically, because that is where you were trying to go. The green message disappears by itself after 5 seconds, or you can click its **×** to close it.

> 💡 **To show a wrong password:** log out, then type a wrong password. A red message **Invalid email or password.** appears and you are not logged in.

### Step 3.2 – Fill in the report form
1. At the top, click the box **I found something**. It turns teal.
2. **Title:** type `Black Umbrella`
3. **Category:** click the menu and choose **Accessories**
4. **Date lost / found:** click the box and pick **today's date** from the calendar.
5. **Location:** type `Main Gate security cabin`
6. **Description:** type `Large black umbrella with a wooden handle, left near the main gate.` The counter below the box shows how many letters you have typed (maximum 1000).
7. **Contact email:** this is already filled with `demo@campus.edu`. Leave it as it is.
8. **Image URL:** leave it empty. It is optional.
9. Click the purple **Submit report** button at the bottom.

✅ **You should see:** a green message **Item reported successfully.** and the detail page of your **Black Umbrella**, with the labels **FOUND** and **OPEN**.

### Step 3.3 – Check that the numbers changed
1. Click **CampusFind** in the top-left corner to go home.

✅ **You should see:** **Total reports** is now **13** and **Found** is now **7**. Your **Black Umbrella** is the first card.

---

## Part 4 – Manage your own item

### Step 4.1 – Change the status
1. Click the **Black Umbrella** card.
2. Scroll down to the section **Manage your listing**. You only see this section because you posted this item.
3. Click the **Status** menu and choose **Claimed**.
4. Click **Update status**.

✅ **You should see:** a green message **Status changed to claimed.** The label changes to blue **CLAIMED**.

5. Repeat steps 3 and 4, this time choosing **Resolved**.

✅ **You should see:** a green **RESOLVED** label. Go back home (click **CampusFind**): the **Resolved** box now shows **3**.

### Step 4.2 – Edit the item
1. Open the **Black Umbrella** item again.
2. Click the **Edit** button.
3. Click the **Title** box, delete the text, and type `Black Umbrella with Wooden Handle`
4. Click the purple **Save changes** button.

✅ **You should see:** a green message **Item updated.** and the new title on the page.

### Step 4.3 – See the form catch mistakes
1. Click **Edit** again.
2. Delete the whole title and type only `ab` (two letters).
3. Click **Save changes**.

✅ **You should see:** a red message **Title must be between 3 and 100 characters.** Nothing is saved. The website checks every field before saving anything.

4. Click **← Back to item** at the top of the form to leave without saving.

### Step 4.4 – Delete the item
1. On the item page, click the red **Delete** button.
2. A small box pops up asking **Delete this listing permanently?** Click **OK**. (Clicking **Cancel** keeps the item.)

✅ **You should see:** the home page with a green message **Item deleted.** and **Total reports** back to **12**.

---

## Part 5 – Show that users cannot touch other people's items

### Step 5.1 – Open someone else's item
1. On the home page, click **Silver Bike Lock Key**. It was posted by another user, **priya.s**.

✅ **You should see:** **no** **Manage your listing** section, and no Edit or Delete buttons. Instead you see a **Contact finder** button.

### Step 5.2 – Try to break in through the address bar
1. Click the browser's address bar. It shows something like `localhost:8000/items/1`.
2. Add `/edit` to the end so that it reads `localhost:8000/items/1/edit`, and press **Return**.

✅ **You should see:** a large **403** with the message **You do not have permission to do that.** Even typing the address directly does not let you edit someone else's post.

3. Click **Back to board**.

### Step 5.3 – Log in as the second user (optional)
1. Click **Log out** in the top-right corner.
2. Click **Log in** and use `priya@campus.edu` with the same password `DemoPassword123!`
3. Open **Silver Bike Lock Key** again. Now **Manage your listing** appears, because Priya posted it.
4. Click **Log out** when done.

---

## Part 6 – Create a brand-new account

1. Click **Sign up** in the top-right corner.
2. Fill in:
   - **Username:** `student1`
   - **Email:** `student1@campus.edu`
   - **Password:** `MyPassword1`
   - **Confirm password:** `MyPassword1`
3. Click **Create account**.

✅ **You should see:** a green message **Welcome to CampusFind, student1!** You are now logged in, and your username shows in the top-right corner.

> 💡 Passwords are never stored as plain text. They are scrambled ("hashed") first, so not even the database owner can read them.

---

## Part 7 – Check the system's health

1. Scroll to the very bottom of any page.
2. In the grey footer, click **System health**.

✅ **You should see:** a short block of text with `"status": "healthy"` and `"database": "connected"`. Automated tools check this page after every release to confirm the site works. If the database ever stopped working, this page would say `"unhealthy"` instead.

3. Click the browser's **Back** button to return.

---

## Part 8 – Phone view

1. Make the browser window very narrow by dragging its right edge to the left until it is about the width of a phone.

✅ **You should see:** the top menu links disappear and a **☰** icon (three lines) appears on the right. Click it to open the menu, and click it again to close it. The cards stack into a single column.

2. Drag the window wide again.

---

## Part 9 – The automatic pipeline on GitHub (browser only)

This part only works **after** the project has been uploaded ("pushed") to GitHub. Everything here happens in the web browser.

### Step 9.1 – Open the pipeline page
1. Go to the project's page on **github.com**.
2. Click the **Actions** tab near the top of the page (between **Pull requests** and **Projects**).
3. In the list, click the newest run, which is the top row.

✅ **You should see:** five boxes joined by lines, from left to right:

| Box | What it does in plain words |
|---|---|
| **1. Unit & integration tests** | A robot runs 22 automatic checks on the website. If any check fails, everything stops here. |
| **2. DevSecOps – Trivy image scan** | A security scanner looks for known weaknesses. Serious problems stop the release. |
| **3. Build & push to GHCR** | The finished app is packed into a box ("container") and stored on GitHub. |
| **4. Deploy** | The new version is sent to the live website. |
| **5. Post-deploy smoke test** | The robot visits the website to confirm it really works. |

A **green tick ✓** means the stage passed. A **red cross ✗** means it failed. A **grey circle** means it was skipped because an earlier stage failed.

### Step 9.2 – Look inside a stage
1. Click the box **1. Unit & integration tests**.
2. Click the line **Run pytest** to expand it.

✅ **You should see:** a list of test names, each ending in **PASSED**, and finally **22 passed**.

3. Go back and click **2. DevSecOps – Trivy image scan**. Scroll down to the **Summary** section to read the security report.

### Step 9.3 – Download the security report
1. On the run's main page, scroll to the bottom to the **Artifacts** section.
2. Click **trivy-report** to download it, then open it from your Downloads folder.

---

## Part 10 – Running the app with Docker Desktop (optional)

This shows the "packaged" version of the app, the same one that goes to the live server.

1. Open the **Docker Desktop** app from your Applications folder. Wait until the whale icon in the top menu bar stops moving.
2. In Terminal, first press **Control + C** to stop the website from Part 1. Then paste this line and press **Return**:

   ```
   docker build -t campusfind:local . && docker run -d --name campusfind -p 8000:5000 -e SECRET_KEY=demo campusfind:local && docker exec campusfind python scripts/seed_demo_data.py
   ```

3. Switch to **Docker Desktop** and click **Containers** in the left sidebar.

✅ **You should see:** a row named **campusfind** with a green dot. After about 30 seconds, its status shows **(healthy)**. Docker checks the health page from Part 7 by itself, every 30 seconds.

4. Click the **8000:5000** link in that row. The website opens in your browser, the same as before.
5. Click the row name **campusfind**, then the **Exec** tab, and type `id` and press **Return**. It shows `uid=10001(appuser)`. This proves the app runs as a restricted user and not as the all-powerful "root" user.
6. When finished, click the **■ Stop** button, then the **🗑 Delete** button on the row.

---

## Part 11 – Switching everything off

1. Go to the Terminal window from Part 1.
2. Press **Control + C**. Use the Control key, **not** Command.

✅ **You should see:** the blinking cursor return. The website is now off, and `localhost:8000` will no longer load.

Every item you posted is saved. It will still be there the next time you start the app.

---

## Quick reference

| What | Value |
|---|---|
| Website address | `localhost:8000` |
| Demo user 1 | `demo@campus.edu` / `DemoPassword123!` |
| Demo user 2 | `priya@campus.edu` / `DemoPassword123!` |
| Health page | `localhost:8000/health` |
| Stop the website | **Control + C** in Terminal |

## If something goes wrong

| Problem | Fix |
|---|---|
| Browser says **"This site can't be reached"** | The Terminal window from Part 1 was closed or stopped. Repeat Steps 1.1–1.3. |
| Terminal says **"Address already in use"** | The app is already running in another Terminal window. Use that one, or close it and try again. |
| Terminal says **"command not found: python3"** | Python is not installed. Download it from python.org, install it, then repeat Step 1.3. |
| Login says **Invalid email or password** | Check the capital letters and the `!` at the end of `DemoPassword123!`. |
| Numbers on the home page differ from this guide | Items were added or deleted earlier. That is fine; the steps still work. To reset to the original 12 items, stop the app and run `source .venv/bin/activate && python scripts/seed_demo_data.py --reset`, then start the app again with Step 1.3. |
| Docker command says **"Cannot connect to the Docker daemon"** | Docker Desktop is not open. Open it and wait for the whale icon to stop moving. |
| Docker says the name **"campusfind" is already in use** | In Docker Desktop → **Containers**, delete the old **campusfind** row, then run the command again. |
