// Main JavaScript for Business Models Website

// Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Check if we're on the homepage or detail page
  const isDetailPage = document.getElementById("modelDetail");

  if (isDetailPage) {
    // Load individual model detail
    loadModelDetail();
  } else {
    // Load all models grid
    loadModelsGrid();
  }
});

/**
 * Load and display all business models in a grid
 */
function loadModelsGrid() {
  const grid = document.getElementById("modelsGrid");

  if (!grid) return;

  // Clear loading message
  grid.innerHTML = "";

  // Create cards for each model
  businessModels.forEach((model) => {
    const card = createModelCard(model);
    grid.appendChild(card);
  });
}

/**
 * Create a model card element
 */
function createModelCard(model) {
  const card = document.createElement("a");
  card.href = `model.html?id=${model.id}`;
  card.className = "model-card";

  // Truncate description to first 150 characters
  const shortDescription = model.howItWorks.substring(0, 150) + "...";

  card.innerHTML = `
    <img
      src="images/${model.image}"
      alt="${model.name}"
      class="model-card-image"
      loading="lazy"
    >
    <div class="model-card-content">
      <div class="model-card-number">Model ${model.id.toString().padStart(2, "0")}</div>
      <h3 class="model-card-title">${model.name}</h3>
      <p class="model-card-description">${shortDescription}</p>
    </div>
  `;

  return card;
}

/**
 * Load individual model detail page
 */
function loadModelDetail() {
  // Get model ID from URL parameter
  const urlParams = new URLSearchParams(window.location.search);
  const modelId = parseInt(urlParams.get("id"));

  if (!modelId || modelId < 1 || modelId > businessModels.length) {
    // Invalid model ID, redirect to homepage
    window.location.href = "index.html";
    return;
  }

  // Find the model (array is 0-indexed, IDs are 1-indexed)
  const model = businessModels[modelId - 1];

  if (!model) {
    window.location.href = "index.html";
    return;
  }

  // Populate the page with model data
  document.getElementById("modelImage").src = `images/${model.image}`;
  document.getElementById("modelImage").alt = model.name;
  document.getElementById("modelNumber").textContent =
    `Model ${model.id.toString().padStart(2, "0")}`;
  document.getElementById("modelTitle").textContent = model.name;
  document.getElementById("howItWorks").textContent = model.howItWorks;
  document.getElementById("origin").textContent = model.origin;
  document.getElementById("examples").textContent = model.examples;
  document.getElementById("whoFor").textContent = model.whoFor;

  // Update page title
  document.title = `${model.name} - Business Models`;

  // Set up navigation buttons
  setupNavigation(modelId);
}

/**
 * Set up previous/next navigation
 */
function setupNavigation(currentId) {
  const prevButton = document.getElementById("prevModel");
  const nextButton = document.getElementById("nextModel");

  // Previous button
  if (currentId > 1) {
    prevButton.href = `model.html?id=${currentId - 1}`;
    prevButton.disabled = false;
  } else {
    prevButton.disabled = true;
    prevButton.style.opacity = "0.3";
    prevButton.style.cursor = "not-allowed";
    prevButton.onclick = (e) => e.preventDefault();
  }

  // Next button
  if (currentId < businessModels.length) {
    nextButton.href = `model.html?id=${currentId + 1}`;
    nextButton.disabled = false;
  } else {
    nextButton.disabled = true;
    nextButton.style.opacity = "0.3";
    nextButton.style.cursor = "not-allowed";
    nextButton.onclick = (e) => e.preventDefault();
  }
}

/**
 * Utility function to truncate text
 */
function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength).trim() + "...";
}
