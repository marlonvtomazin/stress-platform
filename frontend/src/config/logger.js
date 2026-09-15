const LOGGER = {
  enabled: true,

  api: true,
  success: true,
  error: true,
  warning: true,
  debug: false,
};

export function setLogger(config) {
  Object.assign(LOGGER, config);
}

export function logApi(message, data = null) {
  if (!LOGGER.enabled || !LOGGER.api) return;

  console.log(`🌐 API | ${message}`, data ?? "");
}

export function logSuccess(message, data = null) {
  if (!LOGGER.enabled || !LOGGER.success) return;

  console.log(`✅ SUCCESS | ${message}`, data ?? "");
}

export function logError(message, data = null) {
  if (!LOGGER.enabled || !LOGGER.error) return;

  console.error(`❌ ERROR | ${message}`, data ?? "");
}

export function logWarning(message, data = null) {
  if (!LOGGER.enabled || !LOGGER.warning) return;

  console.warn(`⚠️ WARNING | ${message}`, data ?? "");
}

export function logDebug(message, data = null) {
  if (!LOGGER.enabled || !LOGGER.debug) return;

  console.debug(`🐞 DEBUG | ${message}`, data ?? "");
}