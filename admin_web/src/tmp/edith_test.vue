<!DOCTYPE html>

<html lang="zh-CN">

<head>

  <meta charset="UTF-8">

  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>AI工作流模型接入平台</title>

  <style>

    :root {

      --primary-color: #00d4ff;

      --secondary-color: #7e22ce;

      --accent-color: #ff0080;

      --dark-bg: #0f172a;

      --darker-bg: #0a0f1c;

      --text-color: #e2e8f0;

      --card-bg: rgba(30, 41, 59, 0.6);

    }



    * {

      margin: 0;

      padding: 0;

      box-sizing: border-box;

      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;

    }



    body {

      background: linear-gradient(135deg, var(--darker-bg) 0%, var(--dark-bg) 100%);

      color: var(--text-color);

      min-height: 100vh;

      overflow-x: hidden;

    }



    .container {

      max-width: 1400px;

      margin: 0 auto;

      padding: 2rem;

    }



    /* 导航栏样式 */

    .navbar {

      display: flex;

      justify-content: space-between;

      align-items: center;

      padding: 1rem 2rem;

      background: rgba(15, 23, 42, 0.8);

      backdrop-filter: blur(10px);

      border-bottom: 1px solid rgba(255, 255, 255, 0.1);

      position: sticky;

      top: 0;

      z-index: 100;

    }



    .logo {

      font-size: 1.8rem;

      font-weight: 700;

      background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));

      -webkit-background-clip: text;

      background-clip: text;

      color: transparent;

      display: flex;

      align-items: center;

    }



    .logo::before {

      content: "🤖";

      margin-right: 0.5rem;

      font-size: 2rem;

    }



    .nav-links {

      display: flex;

      gap: 2rem;

    }



    .nav-links a {

      color: var(--text-color);

      text-decoration: none;

      font-weight: 500;

      transition: color 0.3s;

      position: relative;

    }



    .nav-links a:hover {

      color: var(--primary-color);

    }



    .nav-links a::after {

      content: '';

      position: absolute;

      bottom: -5px;

      left: 0;

      width: 0;

      height: 2px;

      background: var(--primary-color);

      transition: width 0.3s;

    }



    .nav-links a:hover::after {

      width: 100%;

    }



    /* 主内容区样式 */

    .hero {

      display: flex;

      flex-direction: column;

      align-items: center;

      justify-content: center;

      text-align: center;

      padding: 4rem 2rem;

      min-height: 70vh;

      position: relative;

    }



    .hero::before {

      content: '';

      position: absolute;

      top: 0;

      left: 0;

      right: 0;

      bottom: 0;

      background: radial-gradient(circle at 50% 50%, rgba(126, 34, 206, 0.1) 0%, transparent 50%);

      z-index: -1;

    }



    .hero h1 {

      font-size: 3.5rem;

      margin-bottom: 1.5rem;

      background: linear-gradient(90deg, var(--primary-color), var(--accent-color));

      -webkit-background-clip: text;

      background-clip: text;

      color: transparent;

      line-height: 1.2;

    }



    .hero p {

      font-size: 1.2rem;

      max-width: 700px;

      margin-bottom: 2.5rem;

      color: #cbd5e1;

      line-height: 1.6;

    }



    .cta-buttons {

      display: flex;

      gap: 1rem;

      margin-bottom: 3rem;

    }



    .btn {

      padding: 0.8rem 2rem;

      border-radius: 50px;

      font-weight: 600;

      text-decoration: none;

      transition: all 0.3s;

      border: none;

      cursor: pointer;

      display: inline-flex;

      align-items: center;

      justify-content: center;

    }



    .btn-primary {

      background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));

      color: white;

      box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);

    }



    .btn-primary:hover {

      transform: translateY(-2px);

      box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4);

    }



    .btn-secondary {

      background: transparent;

      color: var(--text-color);

      border: 1px solid rgba(255, 255, 255, 0.2);

    }



    .btn-secondary:hover {

      background: rgba(255, 255, 255, 0.1);

      border-color: var(--primary-color);

    }



    /* 功能卡片区样式 */

    .features {

      display: grid;

      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));

      gap: 2rem;

      margin: 4rem 0;

    }



    .feature-card {

      background: var(--card-bg);

      border-radius: 16px;

      padding: 2rem;

      backdrop-filter: blur(10px);

      border: 1px solid rgba(255, 255, 255, 0.1);

      transition: transform 0.3s, box-shadow 0.3s;

      position: relative;

      overflow: hidden;

    }



    .feature-card::before {

      content: '';

      position: absolute;

      top: -50%;

      left: -50%;

      width: 200%;

      height: 200%;

      background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);

      transform: rotate(45deg);

      transition: all 0.5s;

      opacity: 0;

    }



    .feature-card:hover {

      transform: translateY(-5px);

      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);

    }



    .feature-card:hover::before {

      animation: shine 1.5s;

    }



    @keyframes shine {

      0% {

        opacity: 0;

        transform: rotate(45deg) translate(-50%, -50%);

      }

      50% {

        opacity: 1;

      }

      100% {

        opacity: 0;

        transform: rotate(45deg) translate(50%, 50%);

      }

    }



    .feature-icon {

      font-size: 2.5rem;

      margin-bottom: 1rem;

      background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));

      -webkit-background-clip: text;

      background-clip: text;

      color: transparent;

    }



    .feature-card h3 {

      font-size: 1.5rem;

      margin-bottom: 1rem;

    }



    .feature-card p {

      color: #94a3b8;

      line-height: 1.6;

    }



    /* 数据可视化区域 */

    .stats {

      display: grid;

      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));

      gap: 1.5rem;

      margin: 4rem 0;

    }



    .stat-card {

      background: var(--card-bg);

      border-radius: 12px;

      padding: 1.5rem;

      text-align: center;

      border: 1px solid rgba(255, 255, 255, 0.1);

    }



    .stat-number {

      font-size: 2.5rem;

      font-weight: 700;

      background: linear-gradient(90deg, var(--primary-color), var(--accent-color));

      -webkit-background-clip: text;

      background-clip: text;

      color: transparent;

      margin-bottom: 0.5rem;

    }



    .stat-label {

      color: #94a3b8;

      font-size: 0.9rem;

    }



    /* 页脚样式 */

    footer {

      text-align: center;

      padding: 2rem;

      margin-top: 4rem;

      border-top: 1px solid rgba(255, 255, 255, 0.1);

      color: #94a3b8;

    }



    /* 响应式设计 */

    @media (max-width: 768px) {

      .hero h1 {

        font-size: 2.5rem;

      }



      .cta-buttons {

        flex-direction: column;

      }



      .navbar {

        flex-direction: column;

        gap: 1rem;

      }



      .nav-links {

        gap: 1rem;

        flex-wrap: wrap;

        justify-content: center;

      }

    }



    /* 动画效果 */

    @keyframes float {

      0%, 100% {

        transform: translateY(0);

      }

      50% {

        transform: translateY(-10px);

      }

    }



    .floating {

      animation: float 6s ease-in-out infinite;

    }

  </style>

</head>

<body>

<!-- 导航栏 -->

<nav class="navbar">

  <div class="logo">NeuroFlow AI</div>

  <div class="nav-links">

    <a href="#">首页</a>

    <a href="#">模型库</a>

    <a href="#">工作流</a>

    <a href="#">文档</a>

    <a href="#">社区</a>

  </div>

</nav>



<div class="container">

  <!-- 主内容区 -->

  <section class="hero">

    <h1>智能模型接入平台</h1>

    <p>集成多种AI模型，构建自动化工作流程，释放人工智能的全部潜力</p>

    <div class="cta-buttons">

      <a href="#" class="btn btn-primary">开始使用</a>

      <a href="#" class="btn btn-secondary">查看文档</a>

    </div>

  </section>



  <!-- 功能卡片区 -->

  <section class="features">

    <div class="feature-card">

      <div class="feature-icon">🧠</div>

      <h3>多模型支持</h3>

      <p>无缝接入GPT、Claude、LLaMA等主流AI模型，支持自定义模型扩展</p>

    </div>

    <div class="feature-card">

      <div class="feature-icon">⚡</div>

      <h3>高性能处理</h3>

      <p>基于异步架构和智能负载均衡，实现高并发请求处理和低延迟响应</p>

    </div>

    <div class="feature-card">

      <div class="feature-icon">🔗</div>

      <h3>工作流编排</h3>

      <p>可视化拖拽界面，轻松构建复杂的多模型协作流程和条件逻辑</p>

    </div>

  </section>



  <!-- 数据统计区 -->

  <section class="stats">

    <div class="stat-card">

      <div class="stat-number">15+</div>

      <div class="stat-label">支持的AI模型</div>

    </div>

    <div class="stat-card">

      <div class="stat-number">99.9%</div>

      <div class="stat-label">服务可用性</div>

    </div>

    <div class="stat-card">

      <div class="stat-number">2.5k</div>

      <div class="stat-label">活跃开发者</div>

    </div>

    <div class="stat-card">

      <div class="stat-number">10M+</div>

      <div class="stat-label">日处理请求</div>

    </div>

  </section>

</div>



<footer>

  <p>© 2025 NeuroFlow AI 平台. 构建更智能的未来</p>

</footer>



<script>

  // 添加简单的交互效果

  document.addEventListener('DOMContentLoaded', function() {

    // 为卡片添加随机延迟动画

    const cards = document.querySelectorAll('.feature-card');

    cards.forEach((card, index) => {

      card.style.animationDelay = `${index * 0.2}s`;

    });



    // 数字动画效果

    const statNumbers = document.querySelectorAll('.stat-number');

    statNumbers.forEach(stat => {

      const target = parseInt(stat.textContent);

      let current = 0;

      const increment = target / 50;



      const updateNumber = () => {

        if (current < target) {

          current += increment;

          stat.textContent = Math.round(current);

          setTimeout(updateNumber, 30);

        } else {

          stat.textContent = target;

        }

      };



      // 使用IntersectionObserver实现滚动到视图时触发动画

      const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

          if (entry.isIntersecting) {

            updateNumber();

            observer.unobserve(entry.target);

          }

        });

      });



      observer.observe(stat);

    });

  });

</script>

</body>

</html>
