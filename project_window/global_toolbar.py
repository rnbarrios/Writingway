from PyQt5.QtWidgets import QToolBar, QAction, QWidget, QVBoxLayout, QComboBox, QLabel, QHBoxLayout
from PyQt5.QtGui import QColor
from settings.theme_manager import ThemeManager
from settings.settings_manager import WWSettingsManager
from settings.llm_api_aggregator import WWApiAggregator
from gettext import gettext as _


class GlobalToolbar(QWidget):
    """Global actions toolbar at the top of the window."""
    def __init__(self, controller, tint_color=QColor("black")):
        super().__init__()
        self.controller = controller  # Reference to ProjectWindow for callbacks
        self.tint_color = tint_color
        self.toolbar = QToolBar(_("Global Actions"))
        self.toolbar.setObjectName("GlobalActionsToolBar")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar.setStyleSheet("")  # Reset any custom styles to use theme

        # Create actions and store references
        self.workshop_action = self.add_action("assets/icons/message-square.svg", _("Workshop Chat"), self.controller.open_workshop)
        self.whisper_action = self.add_action("assets/icons/mic.svg", _("Open Whisper"), self.controller.open_whisper_app)
        self.web_llm_action = self.add_action("assets/icons/wikidata.svg", _("Open Web with LLM"), self.controller.open_web_llm)
        self.ia_action = self.add_action("assets/icons/arch.svg", _("Open Internet Archive"), self.controller.open_ia_window)
        self.focus_mode_action = self.add_action("assets/icons/maximize-2.svg", _("Focus Mode"), self.controller.open_focus_mode)

        self.toolbar.addSeparator()

        llm_label = QLabel(_("LLM:"))
        llm_label.setContentsMargins(4, 0, 2, 0)
        self.toolbar.addWidget(llm_label)

        self.provider_combo = QComboBox()
        self.provider_combo.setMinimumWidth(130)
        self.provider_combo.setToolTip(_("Active LLM provider — switch without opening Settings"))
        self._populate_provider_combo()
        self.provider_combo.currentTextChanged.connect(self._on_provider_changed)
        self.toolbar.addWidget(self.provider_combo)

    def add_action(self, icon_path, tooltip, callback):
        action = QAction(ThemeManager.get_tinted_icon(icon_path, self.tint_color), "", self)
        action.setToolTip(tooltip)
        action.triggered.connect(callback)
        self.toolbar.addAction(action)
        return action

    def _populate_provider_combo(self):
        self.provider_combo.blockSignals(True)
        self.provider_combo.clear()
        configs = WWSettingsManager.get_llm_configs()
        active = WWSettingsManager.get_active_llm_name()
        for name in configs:
            self.provider_combo.addItem(name)
        index = self.provider_combo.findText(active)
        if index >= 0:
            self.provider_combo.setCurrentIndex(index)
        self.provider_combo.blockSignals(False)

    def _on_provider_changed(self, name: str):
        if not name:
            return
        WWSettingsManager.set_active_llm_config(name)
        WWApiAggregator.aggregator._provider_cache.clear()

    def refresh_provider_combo(self):
        """Call this after settings are saved to keep the combo in sync."""
        self._populate_provider_combo()

    def update_tint(self, tint_color):
        """Update icon tints when theme changes."""
        self.tint_color = tint_color
        self.workshop_action.setIcon(ThemeManager.get_tinted_icon("assets/icons/message-square.svg", tint_color))
        self.whisper_action.setIcon(ThemeManager.get_tinted_icon("assets/icons/mic.svg", tint_color))
        self.web_llm_action.setIcon(ThemeManager.get_tinted_icon("assets/icons/wikidata.svg", tint_color))
        self.ia_action.setIcon(ThemeManager.get_tinted_icon("assets/icons/arch.svg", tint_color))
        self.focus_mode_action.setIcon(ThemeManager.get_tinted_icon("assets/icons/maximize-2.svg", tint_color))
