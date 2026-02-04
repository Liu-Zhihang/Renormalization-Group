// Fix for long captions in glightbox
// This script ensures long captions are fully displayed with scrolling

document.addEventListener('DOMContentLoaded', function() {
  // Wait for glightbox to initialize
  setTimeout(function() {
    // Add mutation observer to handle dynamically created elements
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        mutation.addedNodes.forEach(function(node) {
          if (node.nodeType === 1) {
            // Check if glightbox container is added
            if (node.classList && node.classList.contains('glightbox-container')) {
              fixCaptions(node);
            }
            // Also check child elements
            const containers = node.querySelectorAll('.glightbox-container');
            containers.forEach(fixCaptions);
          }
        });
      });
    });

    observer.observe(document.body, { childList: true, subtree: true });
  }, 100);
});

function fixCaptions(container) {
  const descriptions = container.querySelectorAll('.gslide-description, .gslide-title, .gdesc-inner');
  descriptions.forEach(function(el) {
    el.style.whiteSpace = 'normal';
    el.style.wordWrap = 'break-word';
    el.style.overflowWrap = 'break-word';
    el.style.maxHeight = 'none';
    el.style.overflow = 'visible';
    el.style.textOverflow = 'unset';
    el.style.display = 'block';
    el.style.webkitLineClamp = 'unset';
  });
  
  // Make description container scrollable if needed
  const descContainer = container.querySelector('.gslide-description');
  if (descContainer) {
    descContainer.style.maxHeight = '40vh';
    descContainer.style.overflowY = 'auto';
    descContainer.style.padding = '16px 24px';
  }
}
