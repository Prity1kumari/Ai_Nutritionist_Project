import { useEffect, useState } from "react";
import { predictFood, askNutritionist } from "./services/api";
import "./App.css";

const initialFood = {
  energy: "",
  fat: "",
  saturated_fat: "",
  carbs: "",
  sugar: "",
  fiber: "",
  protein: "",
  salt: "",
  ingredients: "",
};

function App() {
  const [page, setPage] = useState("dashboard");

  const [food, setFood] = useState(initialFood);
  const [prediction, setPrediction] = useState(null);
  const [predictionLoading, setPredictionLoading] = useState(false);
  const [predictionError, setPredictionError] = useState("");

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);

  const [history, setHistory] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem("nutriai_history");

    if (saved) {
      setHistory(JSON.parse(saved));
    }
  }, []);

  const saveHistory = (result) => {
    const item = {
      id: Date.now(),
      grade: result.health_grade,
      confidence: result.confidence,
      ingredients: food.ingredients,
      date: new Date().toLocaleDateString(),
    };

    const updated = [item, ...history].slice(0, 10);

    setHistory(updated);
    localStorage.setItem(
      "nutriai_history",
      JSON.stringify(updated)
    );
  };

  const handleFoodChange = (e) => {
    const { name, value } = e.target;

    setFood((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const analyzeFood = async (e) => {
    e.preventDefault();

    setPredictionLoading(true);
    setPredictionError("");
    setPrediction(null);

    try {
      const payload = {
        energy: Number(food.energy),
        fat: Number(food.fat),
        saturated_fat: Number(food.saturated_fat),
        carbs: Number(food.carbs),
        sugar: Number(food.sugar),
        fiber: Number(food.fiber),
        protein: Number(food.protein),
        salt: Number(food.salt),
        ingredients: food.ingredients,
      };

      const response = await predictFood(payload);

      setPrediction(response.data);
      saveHistory(response.data);
      setPage("results");
    } catch (error) {
      setPredictionError(
        error.message || "Unable to analyze this food."
      );
    } finally {
      setPredictionLoading(false);
    }
  };

  const sendQuestion = async (e) => {
    e.preventDefault();

    const text = question.trim();

    if (!text || chatLoading) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text,
      },
    ]);

    setQuestion("");
    setChatLoading(true);

    try {
      const result = await askNutritionist(text);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: result.answer,
          sources: result.sources || [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            error.message ||
            "Something went wrong. Please try again.",
          error: true,
        },
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const startNewAnalysis = () => {
    setFood(initialFood);
    setPrediction(null);
    setPredictionError("");
    setPage("analyze");
  };

  return (
    <div className="app-shell">

      <Sidebar
        page={page}
        setPage={setPage}
      />

      <main className="main-content">

        <Topbar page={page} />

        <div className="page-container">

          {page === "dashboard" && (
            <Dashboard
              history={history}
              prediction={prediction}
              onAnalyze={startNewAnalysis}
              onChat={() => setPage("chat")}
              onResults={() => setPage("results")}
            />
          )}

          {page === "analyze" && (
            <AnalyzePage
              food={food}
              handleFoodChange={handleFoodChange}
              analyzeFood={analyzeFood}
              loading={predictionLoading}
              error={predictionError}
            />
          )}

          {page === "results" && prediction && (
            <ResultsPage
              prediction={prediction}
              food={food}
              onAnalyze={startNewAnalysis}
              onChat={() => setPage("chat")}
            />
          )}

          {page === "results" && !prediction && (
            <EmptyResults
              onAnalyze={startNewAnalysis}
            />
          )}

          {page === "chat" && (
            <ChatPage
              messages={messages}
              question={question}
              setQuestion={setQuestion}
              sendQuestion={sendQuestion}
              loading={chatLoading}
            />
          )}

          {page === "history" && (
            <HistoryPage
              history={history}
            />
          )}

        </div>

      </main>

    </div>
  );
}


/* =========================================================
   SIDEBAR
========================================================= */

function Sidebar({ page, setPage }) {
  return (
    <aside className="sidebar">

      <div className="brand">
        <div className="brand-icon">✦</div>

        <div>
          <strong>NutriAI</strong>
          <span>Smart nutrition</span>
        </div>
      </div>

      <nav className="navigation">

        <NavItem
          icon="⌂"
          label="Dashboard"
          active={page === "dashboard"}
          onClick={() => setPage("dashboard")}
        />

        <NavItem
          icon="◉"
          label="Analyze Food"
          active={
            page === "analyze" ||
            page === "results"
          }
          onClick={() => setPage("analyze")}
        />

        <NavItem
          icon="✦"
          label="AI Nutritionist"
          active={page === "chat"}
          onClick={() => setPage("chat")}
        />

        <NavItem
          icon="◷"
          label="History"
          active={page === "history"}
          onClick={() => setPage("history")}
        />

      </nav>

      <div className="sidebar-bottom">

        <div className="ai-status">
          <span className="status-dot"></span>

          <div>
            <strong>AI Online</strong>
            <small>Ready to analyze</small>
          </div>
        </div>

      </div>

    </aside>
  );
}


function NavItem({ icon, label, active, onClick }) {
  return (
    <button
      className={`nav-item ${active ? "active" : ""}`}
      onClick={onClick}
    >
      <span className="nav-icon">{icon}</span>
      <span>{label}</span>
    </button>
  );
}


/* =========================================================
   TOPBAR
========================================================= */

function Topbar({ page }) {
  const titles = {
    dashboard: "Dashboard",
    analyze: "Analyze Food",
    results: "Food Analysis",
    chat: "AI Nutritionist",
    history: "Analysis History",
  };

  return (
    <header className="topbar">

      <div>
        <span className="breadcrumb">
          NutriAI / {titles[page]}
        </span>

        <h2>{titles[page]}</h2>
      </div>

      <div className="profile">
        <div className="avatar">N</div>

        <div className="profile-info">
          <strong>Nutrition User</strong>
          <span>Personal dashboard</span>
        </div>
      </div>

    </header>
  );
}


/* =========================================================
   DASHBOARD
========================================================= */

function Dashboard({
  history,
  onAnalyze,
  onChat,
  onResults,
}) {
  return (
    <div className="fade-in">

      <section className="hero">

        <div className="hero-content">

          <span className="eyebrow">
            ✦ AI-POWERED NUTRITION
          </span>

          <h1>
            Understand your food.
            <br />
            <span>Make better choices.</span>
          </h1>

          <p>
            Analyze nutritional values, identify ingredient
            risks, and ask AI-powered nutrition questions.
          </p>

          <div className="hero-actions">

            <button
              className="button primary"
              onClick={onAnalyze}
            >
              Analyze a food
              <span>→</span>
            </button>

            <button
              className="button secondary"
              onClick={onChat}
            >
              Ask AI
              <span>✦</span>
            </button>

          </div>

        </div>

        <div className="hero-orb">

          <div className="orb-inner">
            <span>✦</span>
          </div>

        </div>

      </section>


      <section className="section">

        <div className="section-header">

          <div>
            <h3>What you can do</h3>
            <p>Powerful nutrition intelligence in one place.</p>
          </div>

        </div>


        <div className="feature-grid">

          <FeatureCard
            icon="◉"
            title="Food Analysis"
            description="Get a health grade based on nutritional composition."
            onClick={onAnalyze}
          />

          <FeatureCard
            icon="⌁"
            title="Ingredient Intelligence"
            description="Understand potential risks hidden in food ingredients."
            onClick={onAnalyze}
          />

          <FeatureCard
            icon="✦"
            title="AI Nutritionist"
            description="Ask questions and receive evidence-based answers."
            onClick={onChat}
          />

        </div>

      </section>


      <section className="section">

        <div className="section-header">

          <div>
            <h3>Recent analyses</h3>
            <p>Your latest food assessments.</p>
          </div>

        </div>

        {history.length === 0 ? (

          <div className="empty-card">

            <div className="empty-icon">◷</div>

            <h3>No analyses yet</h3>

            <p>
              Analyze your first food to see it here.
            </p>

            <button
              className="button primary"
              onClick={onAnalyze}
            >
              Start analyzing
            </button>

          </div>

        ) : (

          <div className="history-grid">

            {history.slice(0, 3).map((item) => (

              <div
                className="history-card"
                key={item.id}
                onClick={onResults}
              >

                <div className="history-top">

                  <GradeBadge
                    grade={item.grade}
                    small
                  />

                  <span>{item.date}</span>

                </div>

                <h4>
                  {item.ingredients || "Food analysis"}
                </h4>

                <p>
                  Confidence{" "}
                  {formatConfidence(item.confidence)}
                </p>

              </div>

            ))}

          </div>

        )}

      </section>

    </div>
  );
}


/* =========================================================
   ANALYZE PAGE
========================================================= */

function AnalyzePage({
  food,
  handleFoodChange,
  analyzeFood,
  loading,
  error,
}) {
  return (
    <div className="fade-in">

      <div className="page-heading">

        <span className="eyebrow">
          FOOD ANALYSIS
        </span>

        <h1>
          Analyze your food
        </h1>

        <p>
          Enter the nutritional information found on the
          product label.
        </p>

      </div>


      <form
        className="analysis-layout"
        onSubmit={analyzeFood}
      >

        <div className="analysis-form card">

          <div className="card-heading">

            <div>
              <h3>Nutrition information</h3>
              <p>Values per 100g</p>
            </div>

            <span className="required">
              Required
            </span>

          </div>


          <div className="nutrition-grid">

            <NutritionInput
              label="Energy"
              name="energy"
              unit="kcal"
              value={food.energy}
              onChange={handleFoodChange}
              placeholder="250"
            />

            <NutritionInput
              label="Fat"
              name="fat"
              unit="g"
              value={food.fat}
              onChange={handleFoodChange}
              placeholder="12.5"
            />

            <NutritionInput
              label="Saturated fat"
              name="saturated_fat"
              unit="g"
              value={food.saturated_fat}
              onChange={handleFoodChange}
              placeholder="4.5"
            />

            <NutritionInput
              label="Carbohydrates"
              name="carbs"
              unit="g"
              value={food.carbs}
              onChange={handleFoodChange}
              placeholder="35"
            />

            <NutritionInput
              label="Sugar"
              name="sugar"
              unit="g"
              value={food.sugar}
              onChange={handleFoodChange}
              placeholder="15"
            />

            <NutritionInput
              label="Fiber"
              name="fiber"
              unit="g"
              value={food.fiber}
              onChange={handleFoodChange}
              placeholder="6"
            />

            <NutritionInput
              label="Protein"
              name="protein"
              unit="g"
              value={food.protein}
              onChange={handleFoodChange}
              placeholder="8"
            />

            <NutritionInput
              label="Salt"
              name="salt"
              unit="g"
              value={food.salt}
              onChange={handleFoodChange}
              placeholder="0.8"
            />

          </div>


          <div className="ingredient-input">

            <label>Ingredients</label>

            <textarea
              name="ingredients"
              value={food.ingredients}
              onChange={handleFoodChange}
              placeholder="Sugar, Palm Oil, Sodium Nitrate..."
              rows="5"
              required
            />

            <span>
              Separate ingredients using commas.
            </span>

          </div>


          {error && (
            <div className="error-box">
              <strong>Analysis failed</strong>
              <span>{error}</span>
            </div>
          )}


          <button
            className="button primary analyze-button"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              <>
                Analyze food
                <span>→</span>
              </>
            )}
          </button>

        </div>


        <div className="preview-card">

          <span className="eyebrow">
            AI ANALYSIS
          </span>

          <h3>
            Your nutrition,
            <br />
            understood.
          </h3>

          <p>
            Our machine-learning model evaluates the
            nutritional composition while our AI analyzes
            the ingredients.
          </p>


          <div className="preview-list">

            <PreviewItem
              icon="◉"
              title="Health grade"
              text="A — E classification"
            />

            <PreviewItem
              icon="⌁"
              title="Ingredient risks"
              text="AI-powered analysis"
            />

            <PreviewItem
              icon="✦"
              title="AI summary"
              text="Personalized explanation"
            />

          </div>

        </div>

      </form>

    </div>
  );
}


/* =========================================================
   RESULTS
========================================================= */

function ResultsPage({
  prediction,
  food,
  onAnalyze,
  onChat,
}) {
  const confidence = Number(prediction.confidence || 0);

  return (
    <div className="fade-in">

      <div className="page-heading result-heading">

        <div>
          <span className="eyebrow">
            ANALYSIS COMPLETE
          </span>

          <h1>
            Here's what we found.
          </h1>

          <p>
            Based on the nutritional profile and ingredients
            you provided.
          </p>
        </div>

        <button
          className="button secondary"
          onClick={onAnalyze}
        >
          Analyze another
        </button>

      </div>


      <section className="result-hero card">

        <div className="grade-section">

          <span className="result-label">
            HEALTH GRADE
          </span>

          <GradeBadge
            grade={prediction.health_grade}
          />

          <p>
            {prediction.health_description}
          </p>

        </div>


        <div className="confidence-section">

          <span className="result-label">
            MODEL CONFIDENCE
          </span>

          <div className="confidence-value">
            {formatConfidence(confidence)}
          </div>

          <div className="progress">
            <div
              className="progress-bar"
              style={{
                width: `${Math.min(
                  confidence * 100,
                  100
                )}%`,
              }}
            />
          </div>

          <p>
            Confidence of the nutrition classification model.
          </p>

        </div>

      </section>


      <section className="section">

        <div className="section-header">

          <div>
            <h3>Nutrition profile</h3>
            <p>Values provided per 100g.</p>
          </div>

        </div>


        <div className="nutrition-result-grid">

          <ResultMetric
            label="Energy"
            value={food.energy}
            unit="kcal"
          />

          <ResultMetric
            label="Fat"
            value={food.fat}
            unit="g"
          />

          <ResultMetric
            label="Saturated fat"
            value={food.saturated_fat}
            unit="g"
          />

          <ResultMetric
            label="Carbohydrates"
            value={food.carbs}
            unit="g"
          />

          <ResultMetric
            label="Sugar"
            value={food.sugar}
            unit="g"
          />

          <ResultMetric
            label="Fiber"
            value={food.fiber}
            unit="g"
          />

          <ResultMetric
            label="Protein"
            value={food.protein}
            unit="g"
          />

          <ResultMetric
            label="Salt"
            value={food.salt}
            unit="g"
          />

        </div>

      </section>


      <section className="section">

        <div className="section-header">

          <div>
            <h3>Ingredient intelligence</h3>
            <p>
              AI-generated insights from the ingredient list.
            </p>
          </div>

        </div>


        <IngredientAnalysis
          data={prediction.ingredient_analysis}
        />

      </section>


      <section className="ai-summary">

        <div className="summary-icon">
          ✦
        </div>

        <div>

          <span className="eyebrow">
            AI SUMMARY
          </span>

          <h3>
            What does this mean?
          </h3>

          <p>
            {prediction.summary}
          </p>

        </div>

      </section>


      <div className="result-actions">

        <button
          className="button primary"
          onClick={onChat}
        >
          Ask AI about this food
          <span>✦</span>
        </button>

        <button
          className="button secondary"
          onClick={onAnalyze}
        >
          Analyze another food
        </button>

      </div>

    </div>
  );
}


/* =========================================================
   CHAT
========================================================= */

function ChatPage({
  messages,
  question,
  setQuestion,
  sendQuestion,
  loading,
}) {
  return (
    <div className="chat-page fade-in">

      <div className="chat-heading">

        <div className="chat-ai-icon">
          ✦
        </div>

        <div>
          <span className="eyebrow">
            AI NUTRITIONIST
          </span>

          <h1>
            Ask anything about food.
          </h1>

          <p>
            Get answers using your nutrition knowledge base
            and supporting documents.
          </p>
        </div>

      </div>


      <div className="chat-container card">

        {messages.length === 0 ? (

          <div className="chat-empty">

            <div className="chat-empty-icon">
              ✦
            </div>

            <h3>
              How can I help?
            </h3>

            <p>
              Ask about ingredients, food safety, nutrition,
              or dietary information.
            </p>


            <div className="suggestions">

              {[
                "Is sodium benzoate safe?",
                "Can children consume MSG?",
                "Is palm oil unhealthy?",
              ].map((item) => (

                <button
                  key={item}
                  onClick={() =>
                    setQuestion(item)
                  }
                >
                  {item}
                </button>

              ))}

            </div>

          </div>

        ) : (

          <div className="messages">

            {messages.map((message, index) => (

              <div
                className={`message-row ${message.role}`}
                key={index}
              >

                <div className="message-avatar">
                  {message.role === "user"
                    ? "N"
                    : "✦"}
                </div>

                <div className="message-content">

                  <span className="message-name">
                    {message.role === "user"
                      ? "You"
                      : "NutriAI"}
                  </span>

                  <div
                    className={`message-bubble ${
                      message.error
                        ? "message-error"
                        : ""
                    }`}
                  >
                    {message.text}
                  </div>



                </div>

              </div>

            ))}


            {loading && (

              <div className="message-row assistant">

                <div className="message-avatar">
                  ✦
                </div>

                <div className="message-content">

                  <span className="message-name">
                    NutriAI
                  </span>

                  <div className="message-bubble typing">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>

                </div>

              </div>

            )}

          </div>

        )}


        <form
          className="chat-composer"
          onSubmit={sendQuestion}
        >

          <input
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            placeholder="Ask a nutrition question..."
          />

          <button
            className="send-button"
            disabled={loading}
          >
            ↑
          </button>

        </form>

      </div>

    </div>
  );
}


/* =========================================================
   HISTORY
========================================================= */

function HistoryPage({ history }) {
  return (
    <div className="fade-in">

      <div className="page-heading">

        <span className="eyebrow">
          HISTORY
        </span>

        <h1>
          Your analyses.
        </h1>

        <p>
          A record of your recent food assessments.
        </p>

      </div>


      {history.length === 0 ? (

        <div className="empty-card">
          <div className="empty-icon">◷</div>

          <h3>
            No history yet
          </h3>

          <p>
            Your completed food analyses will appear here.
          </p>
        </div>

      ) : (

        <div className="history-list">

          {history.map((item) => (

            <div
              className="history-row"
              key={item.id}
            >

              <GradeBadge
                grade={item.grade}
                small
              />

              <div className="history-details">

                <strong>
                  {item.ingredients ||
                    "Food analysis"}
                </strong>

                <span>
                  {item.date}
                </span>

              </div>

              <div className="history-confidence">
                {formatConfidence(item.confidence)}
                <small>confidence</small>
              </div>

            </div>

          ))}

        </div>

      )}

    </div>
  );
}


/* =========================================================
   COMPONENTS
========================================================= */

function NutritionInput({
  label,
  name,
  unit,
  value,
  onChange,
  placeholder,
}) {
  return (
    <div className="modern-field">

      <label htmlFor={name}>
        {label}
      </label>

      <div className="modern-input">

        <input
          id={name}
          type="number"
          min="0"
          step="any"
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required
        />

        <span>{unit}</span>

      </div>

    </div>
  );
}


function GradeBadge({ grade, small = false }) {
  return (
    <div
      className={`grade-badge grade-${String(
        grade
      ).toLowerCase()} ${
        small ? "grade-small" : ""
      }`}
    >
      {grade || "-"}
    </div>
  );
}


function ResultMetric({ label, value, unit }) {
  return (
    <div className="result-metric">

      <span>{label}</span>

      <strong>
        {value}
        <small>{unit}</small>
      </strong>

    </div>
  );
}


function IngredientAnalysis({ data }) {
  if (!data) {
    return (
      <div className="empty-card">
        No ingredient analysis available.
      </div>
    );
  }

  if (!Array.isArray(data)) {
    return (
      <div className="ingredient-single">
        {String(data)}
      </div>
    );
  }

  return (
    <div className="ingredient-grid">

      {data.map((item, index) => (

        <div
          className="ingredient-card"
          key={index}
        >

          <div className="ingredient-icon">
            {getRiskIcon(item.risk)}
          </div>

          <div>

            <h4>
              {item.ingredient}
            </h4>

            <p>
              {item.risk}
            </p>

          </div>

        </div>

      ))}

    </div>
  );
}


function FeatureCard({
  icon,
  title,
  description,
  onClick,
}) {
  return (
    <button
      className="feature-card"
      onClick={onClick}
    >

      <div className="feature-icon">
        {icon}
      </div>

      <h4>{title}</h4>

      <p>{description}</p>

      <span className="feature-arrow">
        →
      </span>

    </button>
  );
}


function PreviewItem({
  icon,
  title,
  text,
}) {
  return (
    <div className="preview-item">

      <div className="preview-icon">
        {icon}
      </div>

      <div>
        <strong>{title}</strong>
        <span>{text}</span>
      </div>

    </div>
  );
}


function EmptyResults({ onAnalyze }) {
  return (
    <div className="empty-page">

      <div className="empty-icon">
        ◉
      </div>

      <h1>
        No analysis yet
      </h1>

      <p>
        Analyze a food to see its nutrition profile here.
      </p>

      <button
        className="button primary"
        onClick={onAnalyze}
      >
        Analyze food
      </button>

    </div>
  );
}


/* =========================================================
   HELPERS
========================================================= */

function formatConfidence(value) {
  const number = Number(value);

  if (number <= 1) {
    return `${(number * 100).toFixed(1)}%`;
  }

  return `${number.toFixed(1)}%`;
}


function getRiskIcon(risk = "") {
  const text = String(risk).toLowerCase();

  if (
    text.includes("high") ||
    text.includes("danger") ||
    text.includes("harmful")
  ) {
    return "!";
  }

  if (
    text.includes("moderate") ||
    text.includes("medium")
  ) {
    return "△";
  }

  return "✓";
}

export default App;