// Video initialization for proper playback (see 注意事项.md)
document.addEventListener('DOMContentLoaded', function() {
  const videos = document.querySelectorAll('video');
  const base = getMkdocsBasePath();
  videos.forEach(video => {
    video.setAttribute('playsinline', '');
    video.setAttribute('preload', 'metadata');

    const sources = video.querySelectorAll('source');
    if (sources.length > 0) {
      sources.forEach(source => {
        const raw = source.getAttribute('src');
        const fixed = normalizeVideoSrc(raw, base);
        if (fixed && fixed !== raw) {
          source.setAttribute('src', fixed);
        }
      });
      video.load();
      return;
    }

    const raw = video.getAttribute('src');
    const fixed = normalizeVideoSrc(raw, base);
    if (fixed && fixed !== raw) {
      video.setAttribute('src', fixed);
      video.load();
    }
  });
});

function getMkdocsBasePath() {
  const configEl = document.getElementById('__config');
  if (!configEl) {
    return '.';
  }
  try {
    const config = JSON.parse(configEl.textContent || '{}');
    return config.base || '.';
  } catch (err) {
    return '.';
  }
}

function normalizeVideoSrc(src, base) {
  if (!src) {
    return src;
  }
  if (/^(?:[a-z]+:)?\/\//i.test(src) || src.startsWith('data:')) {
    return src;
  }

  const marker = 'cn/assets/images/';
  let normalized = src;
  const markerIndex = src.indexOf(marker);
  if (markerIndex !== -1) {
    normalized = src.slice(markerIndex);
  } else {
    const assetIndex = src.indexOf('assets/images/');
    if (assetIndex === -1) {
      return src;
    }
    normalized = 'cn/' + src.slice(assetIndex);
  }

  const trimmedBase = (base && base !== '.') ? base.replace(/\/$/, '') + '/' : '';
  return encodeURI(trimmedBase + normalized);
}
