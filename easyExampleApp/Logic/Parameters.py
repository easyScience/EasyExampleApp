# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

from PySide6.QtCore import QObject, Signal, Slot, Property


class Parameters(QObject):
    asJsonChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pyProxy = parent

        self._as_json = [
            {
                'id': '4538458360',
                'number': 1,
                'label': 'Amplitude',
                'value': self._pyProxy.model.amplitude,
                'unit': '',
                'error': 0.1131,
                'fit': True
            },
            {
                'id': '4092346238',
                'number': 2,
                'label': 'Period',
                'value': self._pyProxy.model.period,
                'unit': 'rad',
                'error': 0.2573,
                'fit': True
            },
            {
                'id': '9834542745',
                'number': 2,
                'label': 'Vertical shift',
                'value': self._pyProxy.model.verticalShift,
                'unit': '',
                'error': 0.0212,
                'fit': True
            },
            {
                'id': '8655377643',
                'number': 2,
                'label': 'Phase shift',
                'value': self._pyProxy.model.phaseShift,
                'unit': 'rad',
                'error': 0.2238,
                'fit': True
            }
        ]

        self.asJsonChanged.connect(self._pyProxy.project.setNeedSaveToTrue)

    @Property('QVariant', notify=asJsonChanged)
    def asJson(self):
        return self._as_json

    @Slot(str, str)
    def editParameterValue(self, pid, value):
        if (pid == '4538458360'):
            self._pyProxy.model.amplitude = float(value)
        elif (pid == '4092346238'):
            self._pyProxy.model.period = float(value)
        elif (pid == '9834542745'):
            self._pyProxy.model.verticalShift = float(value)
        elif (pid == '8655377643'):
            self._pyProxy.model.phaseShift = float(value)
