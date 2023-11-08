# README
#
# =============================================================================
# --- Package structure ---
#
# experiment.py
# │
# ├─ environment.py
# │  ├─ item.py
# │  ├─ ---.py
# │
# ├─ agent.py
# │  ├─ body.py
# │  ├─ energy.py
# │  ├─ processing.py
# │  ├─ perception.py 
# │		├─ innate.py
# │		├─ learning.py
# │  ├─ actuation.py
# │  ├─ nesting.py
# │		├─ communication.py
# │		├─ spacetime.py
# │		├─ ethics.py
# 
# =============================================================================
#
# =============================================================================
# --- Usage ---
#
# - In experiment.py one specific experiment is conducted. 
#   Here the environment and all simulation objects (items, agents) are initialized.
#   The main simulation loop is also performed here.
#
# =============================================================================
#
# =============================================================================
# --- Package conventions ---
#
# - The basic unit for distances is millimeter
# - For code documentation docstrings (Google style) are used.
#
#
# =============================================================================
#
# =============================================================================
# --- Notes ---
#
# - There is one main surface in a simulation
# - A surface is a playground for drawing. Its position is tracked by a rectangle
# - experiments.py is the main module to set all main variables for the experiment
# - workspace.py can start one or more experiments and saves as well as evaluates them
#
# =============================================================================
#