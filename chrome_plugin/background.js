// Listen for bookmark creation
chrome.bookmarks.onCreated.addListener(async (id, bookmark) => {
  try {
    // Get the active tab to fetch page information
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    if (!tab?.id) {
      console.error("No active tab found");
      return;
    }

    // Get domain from the URL
    const url = new URL(bookmark.url);
    const domain = url.hostname;

    // Execute script to extract content based on domain
    const [{ result: extractedData }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (domain) => {
        // Default data
        let data = {
          title: document.title,
          text: "",
        };

        // Try to get meta description for any site
        const metaDescription =
          document.querySelector('meta[name="description"]')?.content ||
          document.querySelector('meta[property="og:description"]')?.content;

        if (metaDescription) {
          data.text = metaDescription;
        }

        // Domain-specific extraction
        if (domain.includes("youtube.com")) {
          // YouTube: Get video description
          const description = document
            .querySelector(
              "#description-inline-expander, .ytd-video-secondary-info-renderer #description"
            )
            ?.textContent?.trim();
          if (description) {
            data.text = description;
          }
        } else if (domain.includes("news.ycombinator.com")) {
          // Hacker News: Get story title and text
          const hnTitle = document.querySelector(".titleline > a")?.textContent;
          if (hnTitle) {
            data.title = hnTitle;
          }

          // Check if it's a story page with text content
          const storyText = document
            .querySelector(".toptext")
            ?.textContent?.trim();
          if (storyText) {
            data.text = storyText;
          } else {
            // If no story text, try to get the first comment or other relevant content
            const firstComment = document
              .querySelector(".comment")
              ?.textContent?.trim();
            if (firstComment) {
              data.text = firstComment;
            }
          }
        }

        return data;
      },
      args: [domain],
    });

    // Prepare the payload
    const payload = {
      src: bookmark.url,
      title: extractedData.title || tab.title,
      text: extractedData.text || "",
    };

    console.log("Sending payload:", payload);

    // Send POST request
    const response = await fetch("http://localhost/api/cards/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log("Card created successfully");
  } catch (error) {
    console.error("Failed to process bookmark:", error);
  }
});
