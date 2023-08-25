const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "https://4614-203-252-223-253.ngrok.io",
      changeOrigin: true,
    })
  );
};
