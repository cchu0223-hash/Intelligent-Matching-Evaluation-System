import { useMemo, useState } from 'react';
import { recommendVoice, submitFeedback } from './api';
import type { FeedbackPayload, Recommendation, RecommendResponse } from './types';

const MAX_TEXT_LENGTH = 15000;
const NAV_ITEMS = [
  { label: '音色匹配', status: 'available' },
  { label: '数字人形象匹配', status: 'coming' },
  { label: '模板匹配', status: 'coming' },
  { label: '背景匹配', status: 'coming' },
  { label: '前景匹配', status: 'coming' },
  { label: '音效匹配', status: 'coming' },
  { label: '音乐匹配', status: 'coming' },
] as const;

type FeedbackState = {
  rating?: number;
  suggestion: string;
  submitted?: boolean;
  status?: string;
};

function asRecord(value: unknown): Record<string, unknown> {
  return value && typeof value === 'object' ? (value as Record<string, unknown>) : {};
}

function renderValue(value: unknown): string {
  if (Array.isArray(value)) {
    return value.length ? value.join('、') : '无';
  }
  if (value && typeof value === 'object') {
    return JSON.stringify(value);
  }
  if (value === null || value === undefined || value === '') {
    return '无';
  }
  return String(value);
}

function tagList(tags: string[], empty = '未标注') {
  if (!tags.length) {
    return <span className="tag tag-muted">{empty}</span>;
  }
  return tags.map((tag) => (
    <span className="tag" key={tag}>
      {tag}
    </span>
  ));
}

function DebugPanel({ response }: { response: RecommendResponse }) {
  const debug = response.debug_tags;
  const l1Hits = asRecord(debug.l1_hits);
  const l2Hits = asRecord(debug.l2_hits);
  const langHits = Array.isArray(debug.lang_hits) ? (debug.lang_hits as string[]) : [];
  const matchedPairs = Array.isArray(debug.matched_pairs) ? debug.matched_pairs.slice(0, 6) : [];

  return (
    <section className="debug-panel" aria-label="匹配调试信息">
      <div className="section-heading">
        <p className="eyebrow">Debug Signals</p>
        <h2>文本识别到的匹配信号</h2>
      </div>
      <div className="debug-grid">
        <div>
          <span>召回阶段</span>
          <strong>{response.stage}</strong>
        </div>
        <div>
          <span>重排模式</span>
          <strong>{response.mode}</strong>
        </div>
        <div>
          <span>语言</span>
          <strong>{langHits.length ? langHits.join('、') : '未命中'}</strong>
        </div>
        <div>
          <span>营销信号</span>
          <strong>{debug.has_marketing_hint ? '是' : '否'}</strong>
        </div>
      </div>
      <div className="signal-columns">
        <div>
          <h3>一级场景</h3>
          <p>{renderValue(Object.keys(l1Hits))}</p>
        </div>
        <div>
          <h3>二级场景</h3>
          <p>{renderValue(Object.keys(l2Hits))}</p>
        </div>
        <div>
          <h3>属性信号</h3>
          <p>
            属性 A {debug.has_child_hint ? '命中' : '未命中'} · 属性 B {debug.has_dialect_hint ? '命中' : '未命中'}
          </p>
        </div>
      </div>
      <div className="matched-keywords">
        {matchedPairs.length ? (
          matchedPairs.map((pair, index) => {
            const item = asRecord(pair);
            return (
              <span key={`${item.scene_l1}-${item.scene_l2}-${index}`}>
                {renderValue(item.scene_l1)} / {renderValue(item.scene_l2)}: {renderValue(item.matched_keywords)}
              </span>
            );
          })
        ) : (
          <span>未命中明确关键词，使用兜底排序。</span>
        )}
      </div>
      {response.llm_error ? <p className="error-text">DeepSeek 重排失败，已回退规则排序：{response.llm_error}</p> : null}
    </section>
  );
}

function RecommendationCard({
  requestId,
  item,
  state,
  onStateChange,
}: {
  requestId: string;
  item: Recommendation;
  state: FeedbackState;
  onStateChange: (next: FeedbackState) => void;
}) {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const canSubmit = Boolean(state.rating) && !isSubmitting;

  async function handleSubmit() {
    if (!state.rating) {
      return;
    }
    setIsSubmitting(true);
    const payload: FeedbackPayload = {
      request_id: requestId,
      vcn: item.vcn,
      speaker_name: item.speaker_name,
      rank: item.rank,
      rating: state.rating,
      suggestion: state.suggestion.trim() || undefined,
    };
    try {
      await submitFeedback(payload);
      onStateChange({ ...state, submitted: true, status: '感谢反馈，已记录你的评价。' });
    } catch (error) {
      onStateChange({ ...state, submitted: false, status: error instanceof Error ? error.message : '提交失败' });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <article className="voice-card">
      <div className="rank-pill">Top {item.rank}</div>
      <div className="voice-card-main">
        <div className="voice-title-row">
          <div>
            <h3>{item.speaker_name}</h3>
            <p>{item.vcn}</p>
          </div>
          <div className="score-badge">{item.score === null ? '内部评分' : item.score.toFixed(2)}</div>
        </div>

        <div className="meta-line">
          <span>{item.gender}</span>
          <span>{item.language || '语言未标注'}</span>
          <span>{item.tech_desc || '技术标签未标注'}</span>
        </div>

        <div className="tag-group" aria-label="一级场景标签">
          <span className="tag-label">一级</span>
          {tagList(item.scene_l1)}
        </div>
        <div className="tag-group" aria-label="二级场景标签">
          <span className="tag-label">二级</span>
          {tagList(item.scene_l2)}
        </div>
        <div className="tag-group" aria-label="属性标签">
          <span className="tag-label">属性</span>
          {tagList(item.attributes)}
        </div>

        <div className="reason-box">
          <span>推荐依据</span>
          <p>{item.reason || '规则召回排序'}</p>
        </div>

        <div className="audio-area">
          {item.audio_url ? (
            <audio controls src={item.audio_url}>
              当前浏览器不支持音频播放。
            </audio>
          ) : (
            <div className="audio-placeholder">待接入试听 URL</div>
          )}
        </div>
      </div>

      <div className="feedback-box">
        {state.submitted ? (
          <div className="feedback-success" role="status">
            <span>感谢反馈</span>
            <p>已记录你的评价。</p>
          </div>
        ) : (
          <>
            <label>这个音色适合当前文本吗？</label>
            <div className="rating-row" role="group" aria-label={`${item.speaker_name} 评分`}>
              {[1, 2, 3, 4, 5].map((rating) => (
                <button
                  className={state.rating === rating ? 'rating-button active' : 'rating-button'}
                  key={rating}
                  type="button"
                  onClick={() => onStateChange({ ...state, rating, submitted: false, status: undefined })}
                >
                  {rating}
                </button>
              ))}
            </div>
            <textarea
              aria-label={`${item.speaker_name} 文字建议`}
              maxLength={2000}
              placeholder="可选：为什么适合或不适合？"
              value={state.suggestion}
              onChange={(event) => onStateChange({ ...state, suggestion: event.target.value, submitted: false, status: undefined })}
            />
            <button className="secondary-button" disabled={!canSubmit} type="button" onClick={handleSubmit}>
              {isSubmitting ? '提交中' : '提交反馈'}
            </button>
            {state.status ? <p className="feedback-status">{state.status}</p> : null}
          </>
        )}
      </div>
    </article>
  );
}

export default function App() {
  const [text, setText] = useState('');
  const [response, setResponse] = useState<RecommendResponse | null>(null);
  const [feedback, setFeedback] = useState<Record<string, FeedbackState>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const remaining = MAX_TEXT_LENGTH - text.length;
  const canRecommend = text.trim().length > 0 && remaining >= 0 && !isLoading;
  const sortedRecommendations = useMemo(() => response?.recommendations ?? [], [response]);

  async function handleRecommend() {
    setIsLoading(true);
    setError(null);
    setResponse(null);
    setFeedback({});
    try {
      const next = await recommendVoice(text);
      setResponse(next);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : '请求失败');
    } finally {
      setIsLoading(false);
    }
  }

  function handleClearText() {
    setText('');
    setError(null);
  }

  return (
    <div className="app-frame">
      <aside className="sidebar" aria-label="评测模块导航">
        <div className="brand-block">
          <div className="brand-mark" aria-hidden="true">讯</div>
          <div className="brand-copy">
            <span>讯飞智作</span>
            <strong>智能评测系统</strong>
          </div>
        </div>
        <nav className="nav-list">
          {NAV_ITEMS.map((item) => {
            const isAvailable = item.status === 'available';
            return (
              <button
                className={isAvailable ? 'nav-item active' : 'nav-item disabled'}
                disabled={!isAvailable}
                key={item.label}
                type="button"
                aria-current={isAvailable ? 'page' : undefined}
              >
                <span className="nav-dot" aria-hidden="true" />
                <span className="nav-label">{item.label}</span>
                <span className="nav-status">{isAvailable ? '当前' : '待开放'}</span>
              </button>
            );
          })}
        </nav>
      </aside>

      <main className="app-shell">
        <section className="hero-band">
          <div>
            <p className="eyebrow">Voice Matching Lab</p>
            <h1>音色智能匹配评测台</h1>
            <p className="hero-copy">
              输入真实配音文本，系统返回去重后的 Top5 音色，并收集每个推荐的评分与建议。当前版本聚焦“文本到音色标签匹配”，保留扩展到更多智能评测任务的数据结构。
            </p>
          </div>
          <div className="status-strip" aria-label="系统能力">
            <span>Top5 推荐</span>
            <span>15000 字上限</span>
            <span>规则召回 + DeepSeek 重排</span>
          </div>
        </section>

        <section className="composer">
          <div className="composer-header">
            <div>
              <p className="eyebrow">Input</p>
              <h2>配音文本</h2>
            </div>
            <div className="composer-tools">
              <button className="ghost-button" disabled={!text.length || isLoading} type="button" onClick={handleClearText}>
                清空
              </button>
              <span className={remaining < 0 ? 'counter danger' : 'counter'}>{text.length} / {MAX_TEXT_LENGTH}</span>
            </div>
          </div>
          <textarea
            className="script-input"
            placeholder="粘贴一段真实配音文本，用于评测系统推荐出的音色是否合适。"
            value={text}
            onChange={(event) => setText(event.target.value)}
          />
          <div className="action-row">
            <button className="primary-button" disabled={!canRecommend} type="button" onClick={handleRecommend}>
              {isLoading ? '匹配中' : '智能匹配'}
            </button>
            <p>{remaining < 0 ? `已超出 ${Math.abs(remaining)} 字` : '模型分析会使用截断文本，但完整输入会进入评测记录。'}</p>
          </div>
          {error ? <p className="error-text">{error}</p> : null}
        </section>

        {response ? <DebugPanel response={response} /> : null}

        {response && sortedRecommendations.length ? (
          <section className="recommendations" aria-label="推荐音色">
            <div className="section-heading">
              <p className="eyebrow">Recommendations</p>
              <h2>去重后 Top5 音色</h2>
            </div>
            <div className="voice-list">
              {sortedRecommendations.map((item) => (
                <RecommendationCard
                  item={item}
                  key={`${response.request_id}-${item.vcn}-${item.rank}`}
                  requestId={response.request_id}
                  state={feedback[item.vcn] || { suggestion: '' }}
                  onStateChange={(next) => setFeedback((current) => ({ ...current, [item.vcn]: next }))}
                />
              ))}
            </div>
          </section>
        ) : null}
      </main>
    </div>
  );
}
