import React from 'react'
import {
    GaugeContainer,
    GaugeReferenceArc,
    GaugeValueArc,
    GaugeValueText,
} from '@mui/x-charts/Gauge';

// Infos que deve receber
// Porcentagem, Texto a ser exibido, arco dividido ou inteiro?

const ArcGauge = ( {value = 50, isFull = false } ) => {
    const startAngle = isFull ? 0 : -90;
    const endAngle = isFull ? 360 : 90;

    return (
        <GaugeContainer value={value}
            valueMax={100}
            startAngle={startAngle}
            endAngle={endAngle}
            cornerRadius={'50%'}

        >
            <GaugeReferenceArc />
            <GaugeValueArc sx={{ fill: (theme) => theme.palette.admin.main }} />

            <GaugeValueText
                text={`${value}%`}
                sx={(theme) => ({
                    fontSize: '1.5em',
                    fontWeight: theme => theme.typograpy.fontWeightRegular,
                    fontFamily: theme => theme.typograpy.fontFamily,
                    transform: isFull ? 'translate(0, 0)' : 'translate(0, 20px)',
                    '& tspan': {
                        fill: theme.palette.text.primary, 
                    },
                })}
            />
        </GaugeContainer>
    )
}

export default ArcGauge