export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);
    const url = new URL(request.url);

    // Keep the workers.dev validation hostname out of search indexes.
    if (!url.hostname.endsWith(".workers.dev")) return response;

    const headers = new Headers(response.headers);
    headers.set("x-robots-tag", "noindex, nofollow");
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
