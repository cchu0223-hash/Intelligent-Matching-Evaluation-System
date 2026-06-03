# Frontend

React + Vite evaluation page for entering dubbing text, viewing Top5 voice recommendations, playing sample audio, and submitting rating feedback.

## Features

- Real dubbing text input with 15000 character limit.
- Top5 voice recommendation display.
- Debug information for 一级场景、二级场景、属性信号、语言、召回阶段、重排模式.
- Per-voice tag display: 一级场景、二级场景、属性标签、性别、语言、技术标签.
- Audio player placeholder for future voice sample URLs.
- Per-voice 1-5 rating and optional suggestion submission.

## Local Run

```bash
npm install
npm run dev
```

Set `VITE_API_BASE_URL` if the backend is not running on `http://localhost:8000`.

## Build

```bash
npm run build
```
