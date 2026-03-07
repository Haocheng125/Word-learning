// Cloudflare Pages Worker
// 这个文件告诉 Cloudflare 这是一个前端项目
// 所有请求都返回静态资源

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // 尝试获取静态资源
    const response = await env.ASSETS.fetch(request);
    
    // 如果是 404 且不是文件请求，返回 index.html（SPA 支持）
    if (response.status === 404 && !url.pathname.includes('.')) {
      return env.ASSETS.fetch(`${url.origin}/index.html`);
    }
    
    return response;
  }
};
