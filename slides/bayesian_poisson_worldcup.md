# Bayesian Poisson Model for World Cup Goals

Positioning:

> This presentation builds from our friend's draft and research, then sharpens the concept into a clear Bayesian Poisson case study using World Cup goal counts.

Main idea:

> We are not building a football prediction AI first. We are using football data to explain Bayesian inference for count data.

---

# Motivation

Football goals are count data:

- 0 goals
- 1 goal
- 2 goals
- 3 goals
- and so on

Because goals are non-negative integers, the Poisson distribution is a natural starting point.

The World Cup dataset gives us a real example for explaining the math.

---

# Research Question

Primary question:

> How can a Bayesian Poisson model be used to model the number of goals in a World Cup match?

Secondary demonstration:

> If we learn from World Cups 2010, 2014, and 2018, are the goal counts in World Cup 2022 plausible under the model?

---

# Why Poisson?

A Poisson distribution models the number of events in a fixed interval.

For this project:

- event: a goal
- interval: one football match
- random variable: total goals in a match

Let:

$$
Y = \text{total goals in one match}
$$

Then:

$$
Y \sim \text{Poisson}(\lambda)
$$

---

# Poisson Distribution

The probability of observing exactly \( y \) goals is:

$$
P(Y = y \mid \lambda) =
\frac{e^{-\lambda}\lambda^y}{y!}
$$

Where:

- \( y \): observed number of goals
- \( \lambda \): expected goals per match
- \( \lambda > 0 \)

If \( \lambda = 2.5 \), the model expects about 2.5 goals per match.

---

# What Bayesian Adds

In a basic Poisson model, \( \lambda \) is an unknown fixed value.

In Bayesian inference, \( \lambda \) is uncertain.

Instead of asking:

> What is the single best estimate of \( \lambda \)?

We ask:

> What do we believe about \( \lambda \), after seeing the data?

---

# Bayes Theorem

Bayesian inference is based on:

$$
P(\theta \mid data) =
\frac{P(data \mid \theta)P(\theta)}{P(data)}
$$

For this project:

$$
P(\lambda \mid data)
\propto
P(data \mid \lambda)P(\lambda)
$$

In words:

```text
Posterior belief = likelihood from data x prior belief
```

---

# Prior Distribution

Before observing the World Cup data, we assign a prior belief about \( \lambda \).

Because \( \lambda \) must be positive, we use a Gamma prior:

$$
\lambda \sim \text{Gamma}(\alpha, \beta)
$$

Where:

- \( \alpha \): shape parameter
- \( \beta \): rate parameter
- prior mean:

$$
E[\lambda] = \frac{\alpha}{\beta}
$$

---

# Why Gamma Prior?

The Gamma distribution is useful because:

- it only allows positive values
- it is flexible
- it is conjugate to the Poisson likelihood

Conjugate means:

> If the prior is Gamma and the likelihood is Poisson, then the posterior is also Gamma.

This makes the math clean and suitable for a Mathematical and Statistical Foundations assignment.

---

# Why This Prior?

In the notebook we use:

$$
\lambda \sim \text{Gamma}(5, 2)
$$

The prior mean is:

$$
E[\lambda] = \frac{5}{2} = 2.5
$$

Why this prior?

- modern World Cup matches usually average around 2 to 3 goals
- 2.5 is a reasonable starting belief before seeing the training data
- the prior is weak compared with 192 training matches from 2010-2018

So the prior guides the model, but the data still dominates the posterior.

---

# Likelihood From Match Data

Suppose we observe \( n \) matches:

$$
y_1, y_2, ..., y_n
$$

Each match goal count follows:

$$
Y_i \sim \text{Poisson}(\lambda)
$$

The important data summaries are:

- total goals: \( \sum y_i \)
- number of matches: \( n \)

---

# Posterior Distribution

With a Gamma prior and Poisson likelihood:

$$
\lambda \mid data
\sim
\text{Gamma}(\alpha + \sum y_i, \beta + n)
$$

So:

$$
\alpha_{post} = \alpha + \sum y_i
$$

$$
\beta_{post} = \beta + n
$$

Posterior mean:

$$
E[\lambda \mid data] =
\frac{\alpha_{post}}{\beta_{post}}
$$

---

# Prediction

After estimating the posterior, we can predict goals in a future match.

Bayesian prediction gives a probability distribution:

```text
P(next match has 0 goals)
P(next match has 1 goal)
P(next match has 2 goals)
P(next match has 3 goals)
...
```

This is called the posterior predictive distribution.

It is better than giving only one predicted value because it includes uncertainty.

---

# Dataset Plan

Training data:

```text
World Cup 2010
World Cup 2014
World Cup 2018
```

Testing data:

```text
World Cup 2022
```

Reason:

- 2022 is complete
- modern World Cups have similar scoring patterns
- very old tournaments had different formats and scoring behavior

---

# Evaluation

Because the model predicts counts, the main evaluation should also be count-based.

Useful checks:

- compare predicted mean goals with actual 2022 average
- compute mean absolute error
- compute root mean squared error
- check whether actual 2022 goal counts are plausible under the posterior predictive distribution

Optional classification:

```text
Positive = over 2.5 goals
Negative = 2 or fewer goals
```

Then we can create true positive, false positive, true negative, and false negative counts.

---

# Actual 2022 vs Model Prediction

The notebook compares actual 2022 goal-count frequencies with predicted probability from the posterior predictive distribution.

Example interpretation:

```text
If the model gives high probability to 2 or 3 goals,
then many 2022 matches with 2 or 3 goals are plausible.
```

We also compare two training choices:

```text
Recent model: 2010-2018
Historical model: 1930-2018
```

This helps explain why very old World Cup data may not always be the best guide for modern football.

---

# Strengths and Limitations

Strengths:

- simple mathematical structure
- suitable for count data
- demonstrates prior, likelihood, posterior, and prediction
- easy to reproduce in Jupyter

Limitations:

- all matches share one average goal rate
- team strength is ignored
- opponent strength is ignored
- group and knockout matches are treated the same
- goals may not be perfectly independent

---

# Conclusion

The Bayesian Poisson model is a clear way to explain count-data modeling.

For this assignment:

- Poisson models total goals per match
- Bayesian inference updates uncertainty about \( \lambda \)
- Gamma prior gives a clean conjugate posterior
- World Cup data provides a real demonstration
- Jupyter shows the end-to-end calculation

Final framing:

> We polish the draft into a focused statistical explanation, then support it with a reproducible World Cup notebook.
