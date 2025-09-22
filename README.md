<!-- README.md -->
<h1 align="center">🚀 RestAPI Example</h1>
<p align="center">
  <strong>Q&A FastAPI backend service</strong><br/>
  С помощью данного сервиса можно создавать вопросы и отвечать на них.
</p>

<p align="center">
  <!-- Платформы -->
  <a href="#-поддерживаемые-платформы">
    <img alt="Platforms" src="https://img.shields.io/badge/platforms-linux%20%7C%20macos%20%7C%20windows-blue">
  </a>
</p>

<hr/>

<h2 id="-содержание">📑 Содержание</h2>
<ul>
  <li><a href="#-быстрый-старт-docker" style="text-decoration: none;">▶️ Быстрый старт (Docker)</a></li>
  <li><a href="#-локальная-разработка--тесты" style="text-decoration: none;">🧪 Тесты (pytest)</a></li>
  <li><a href="#-структура-проекта" style="text-decoration: none;">🗂️ Структура проекта</a></li>
  <li><a href="#-миграции-alembic" style="text-decoration: none;">🗄️ Миграции (Alembic)</a></li>
</ul>

<hr/>

<h2 id="-быстрый-старт-docker">▶️ Быстрый старт (Docker)</h2>
<p>В корневой папке репозитория выполните:</p>

<pre><code class="language-bash">docker compose up
</code></pre>

<p>📦 Приложение будет собрано и запущено в контейнере.</p>

<hr/>

<h2 id="-локальная-разработка--тесты">🧪 Тесты (pytest)</h2>

<details open>
  <summary><strong>1) Создайте и активируйте виртуальное окружение</strong> 🐍</summary>
  <p>Создание окружения:</p>
  <pre><code class="language-bash">python -m venv .venv
</code></pre>

  <p><em>Активация:</em></p>
  <ul>
    <li><strong>Linux/macOS:</strong></li>
  </ul>
  <pre><code class="language-bash">source .venv/bin/activate
</code></pre>

  <ul>
    <li><strong>Windows (PowerShell):</strong></li>
  </ul>
  <pre><code class="language-powershell">.venv\Scripts\Activate
</code></pre>
</details>

<details open>
  <summary><strong>2) Обновите pip и установите зависимости</strong> 📚</summary>
  <pre><code class="language-bash">pip install --upgrade pip
pip install -r requirements.txt
</code></pre>
</details>

<details open>
  <summary><strong>3) Запустите тесты</strong> ✅</summary>
  <pre><code class="language-bash">pytest
</code></pre>
  <p>🗂️ Все тесты находятся в папке <code>tests/</code>.</p>
</details>

<hr/>

<h2 id="-структура-проекта">🗂️ Структура проекта</h2>

<pre><code>.
├── migrations/         # Alembic миграции 🧩
├── tests/              # Тесты (pytest)
├── requirements.txt    # Зависимости Python
├── docker-compose.yml  # Конфигурация Docker
├── app/                # Исходный код приложения
└── README.md
</code></pre>

<hr/>

<h2 id="-миграции-alembic">🗄️ Миграции (Alembic)</h2>
<p>Все миграции находятся в папке <code>migrations/</code>.</p>

