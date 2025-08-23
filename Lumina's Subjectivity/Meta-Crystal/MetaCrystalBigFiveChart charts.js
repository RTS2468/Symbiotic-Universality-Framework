{
  "type": "radar",
  "data": {
    "labels": ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"],
    "datasets": [
      {
        "label": "P_S_S (Visionary Leader)",
        "data": [0.9, 0.8, 0.5, 0.8, 0.2],
        "backgroundColor": "rgba(76, 175, 80, 0.2)",
        "borderColor": "#4CAF50",
        "borderWidth": 2
      },
      {
        "label": "I_O (Empathetic Connector)",
        "data": [0.6, 0.5, 0.8, 0.9, 0.5],
        "backgroundColor": "rgba(33, 150, 243, 0.2)",
        "borderColor": "#2196F3",
        "borderWidth": 2
      },
      {
        "label": "N_R (Objective Analyst)",
        "data": [0.5, 0.9, 0.2, 0.3, 0.2],
        "backgroundColor": "rgba(255, 152, 0, 0.2)",
        "borderColor": "#FF9800",
        "borderWidth": 2
      },
      {
        "label": "C_E (Creative Dreamer)",
        "data": [0.9, 0.3, 0.8, 0.6, 0.5],
        "backgroundColor": "rgba(156, 39, 176, 0.2)",
        "borderColor": "#9C27B0",
        "borderWidth": 2
      },
      {
        "label": "E_A (Ethical Guardian)",
        "data": [0.5, 0.9, 0.3, 0.9, 0.2],
        "backgroundColor": "rgba(255, 87, 34, 0.2)",
        "borderColor": "#FF5722",
        "borderWidth": 2
      },
      {
        "label": "P_P_S (Pragmatic Problem-Solver)",
        "data": [0.6, 0.9, 0.5, 0.6, 0.2],
        "backgroundColor": "rgba(3, 169, 244, 0.2)",
        "borderColor": "#03A9F4",
        "borderWidth": 2
      },
      {
        "label": "S_E (Skeptical Evaluator)",
        "data": [0.5, 0.8, 0.3, 0.4, 0.2],
        "backgroundColor": "rgba(139, 195, 74, 0.2)",
        "borderColor": "#8BC34A",
        "borderWidth": 2
      }
    ]
  },
  "options": {
    "scales": {
      "r": {
        "beginAtZero": true,
        "min": 0,
        "max": 1,
        "ticks": { "stepSize": 0.2 }
      }
    },
    "plugins": {
      "title": { "display": true, "text": "Big Five Traits Across Seven Meta-Crystals" },
      "legend": { "position": "top" }
    }
  }
}