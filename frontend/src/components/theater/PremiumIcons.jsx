import React from 'react';

/**
 * Premium SVG Icons - Best Practices Implementation
 * - Optimized viewBox (24x24 standard)
 * - Crisp stroke widths (1.5-2px)
 * - Proper scaling without distortion
 * - Subtle gradients and effects
 */

// Shared gradient definitions
const GoldGradient = ({ id }) => (
    <linearGradient id={id} x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#FFD700" />
        <stop offset="100%" stopColor="#B8860B" />
    </linearGradient>
);

const GlowFilter = ({ id, color = "#D4AF37" }) => (
    <filter id={id} x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="1" result="blur" />
        <feFlood floodColor={color} floodOpacity="0.3" />
        <feComposite in2="blur" operator="in" />
        <feMerge>
            <feMergeNode />
            <feMergeNode in="SourceGraphic" />
        </feMerge>
    </filter>
);

/**
 * IluminateLogo - Clean pyramid with eye
 * Standard 24x24 viewBox, scales cleanly
 */
export const IluminateLogo = ({
    size = 24,
    animated = false,
    className = ''
}) => {
    const id = React.useId();

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
            xmlns="http://www.w3.org/2000/svg"
        >
            <defs>
                <GoldGradient id={`${id}-gold`} />
                <GlowFilter id={`${id}-glow`} />
            </defs>

            <g filter={`url(#${id}-glow)`}>
                {/* Pyramid */}
                <path
                    d="M12 2L22 20H2L12 2Z"
                    fill="none"
                    stroke={`url(#${id}-gold)`}
                    strokeWidth="1.5"
                    strokeLinejoin="round"
                />

                {/* Eye */}
                <ellipse
                    cx="12"
                    cy="12"
                    rx="4"
                    ry="2.5"
                    fill="none"
                    stroke={`url(#${id}-gold)`}
                    strokeWidth="1.5"
                />

                {/* Pupil */}
                <circle
                    cx="12"
                    cy="12"
                    r="1.5"
                    fill={`url(#${id}-gold)`}
                >
                    {animated && (
                        <animate
                            attributeName="r"
                            values="1.5;2;1.5"
                            dur="2s"
                            repeatCount="indefinite"
                        />
                    )}
                </circle>
            </g>
        </svg>
    );
};

/**
 * CompanyIcon - Clean building icon
 */
export const CompanyIcon = ({
    size = 24,
    color = '#D4AF37',
    risk = false,
    className = ''
}) => {
    const id = React.useId();
    const mainColor = risk ? '#ef4444' : color;

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GlowFilter id={`${id}-glow`} color={mainColor} />
            </defs>

            <g filter={`url(#${id}-glow)`} stroke={mainColor} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                {/* Main Building */}
                <rect x="3" y="9" width="8" height="12" rx="1" />

                {/* Tower */}
                <rect x="11" y="3" width="10" height="18" rx="1" />

                {/* Windows Main */}
                <rect x="5" y="11" width="2" height="2" fill={mainColor} />
                <rect x="5" y="15" width="2" height="2" fill={mainColor} />

                {/* Windows Tower */}
                <rect x="14" y="6" width="2" height="2" fill={mainColor} />
                <rect x="14" y="10" width="2" height="2" fill={mainColor} />
                <rect x="14" y="14" width="2" height="2" fill={mainColor} />

                {/* Door */}
                <rect x="17" y="17" width="2" height="4" fill={mainColor} />
            </g>

            {/* Risk Indicator */}
            {risk && (
                <circle cx="20" cy="4" r="3" fill="#ef4444" stroke="#0A0A0A" strokeWidth="1">
                    <animate attributeName="opacity" values="1;0.6;1" dur="1s" repeatCount="indefinite" />
                </circle>
            )}
        </svg>
    );
};

/**
 * PersonIcon - Clean person silhouette
 */
export const PersonIcon = ({
    size = 24,
    color = '#60a5fa',
    className = ''
}) => {
    const id = React.useId();

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GlowFilter id={`${id}-glow`} color={color} />
            </defs>

            <g filter={`url(#${id}-glow)`} stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                {/* Head */}
                <circle cx="12" cy="7" r="4" />

                {/* Body */}
                <path d="M5 21v-2a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v2" />

                {/* Tie detail */}
                <path d="M12 14v4" stroke={color} strokeWidth="1" opacity="0.5" />
            </g>
        </svg>
    );
};

/**
 * LocationIcon - Clean map pin
 */
export const LocationIcon = ({
    size = 24,
    color = '#34d399',
    virtual = false,
    className = ''
}) => {
    const id = React.useId();
    const mainColor = virtual ? '#fbbf24' : color;

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GlowFilter id={`${id}-glow`} color={mainColor} />
            </defs>

            <g filter={`url(#${id}-glow)`} stroke={mainColor} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                {/* Pin */}
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" />

                {/* Inner circle */}
                <circle cx="12" cy="9" r="2.5" fill={mainColor} />
            </g>

            {/* Virtual indicator */}
            {virtual && (
                <g>
                    <circle cx="18" cy="6" r="4" fill="#fbbf24" stroke="#0A0A0A" strokeWidth="1" />
                    <text x="18" y="8" textAnchor="middle" fill="#0A0A0A" fontSize="6" fontWeight="bold">V</text>
                </g>
            )}
        </svg>
    );
};

/**
 * RiskIcon - Clean warning triangle
 */
export const RiskIcon = ({
    size = 24,
    level = 5,
    className = ''
}) => {
    const id = React.useId();
    const color = level > 7 ? '#ef4444' : level > 4 ? '#fbbf24' : '#34d399';

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GlowFilter id={`${id}-glow`} color={color} />
            </defs>

            <g filter={`url(#${id}-glow)`} stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                {/* Triangle */}
                <path d="M12 2L22 20H2L12 2Z" fill={`${color}20`} />

                {/* Exclamation */}
                <line x1="12" y1="9" x2="12" y2="13" strokeWidth="2" />
                <circle cx="12" cy="16" r="1" fill={color} />
            </g>
        </svg>
    );
};

/**
 * VaultDoorIcon - Clean vault/safe icon
 */
export const VaultDoorIcon = ({
    size = 24,
    spinning = false,
    className = ''
}) => {
    const id = React.useId();

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GoldGradient id={`${id}-gold`} />
                <GlowFilter id={`${id}-glow`} />
            </defs>

            <g filter={`url(#${id}-glow)`}>
                {/* Outer ring */}
                <circle
                    cx="12"
                    cy="12"
                    r="10"
                    stroke={`url(#${id}-gold)`}
                    strokeWidth="2"
                    fill="none"
                />

                {/* Handle group */}
                <g stroke={`url(#${id}-gold)`} strokeWidth="2" strokeLinecap="round">
                    {spinning && (
                        <animateTransform
                            attributeName="transform"
                            type="rotate"
                            from="0 12 12"
                            to="360 12 12"
                            dur="2s"
                            repeatCount="indefinite"
                        />
                    )}

                    {/* Cross handle */}
                    <line x1="6" y1="12" x2="18" y2="12" />
                    <line x1="12" y1="6" x2="12" y2="18" />

                    {/* Center */}
                    <circle cx="12" cy="12" r="3" fill={`url(#${id}-gold)`} />
                </g>
            </g>
        </svg>
    );
};

/**
 * StampIcon - Clean seal/stamp icon
 */
export const StampIcon = ({
    size = 24,
    className = ''
}) => {
    const id = React.useId();

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GoldGradient id={`${id}-gold`} />
                <GlowFilter id={`${id}-glow`} />
            </defs>

            <g filter={`url(#${id}-glow)`} stroke={`url(#${id}-gold)`} strokeWidth="1.5">
                {/* Outer circle */}
                <circle cx="12" cy="12" r="9" />

                {/* Inner circle */}
                <circle cx="12" cy="12" r="6" />

                {/* Check mark */}
                <path d="M8 12l2.5 2.5L16 9" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </g>
        </svg>
    );
};

/**
 * DatabaseIcon - Clean database cylinder
 */
export const DatabaseIcon = ({
    size = 24,
    scanning = false,
    className = ''
}) => {
    const id = React.useId();

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GoldGradient id={`${id}-gold`} />
                <GlowFilter id={`${id}-glow`} />
            </defs>

            <g filter={`url(#${id}-glow)`} stroke={`url(#${id}-gold)`} strokeWidth="1.5">
                {/* Top ellipse */}
                <ellipse cx="12" cy="5" rx="8" ry="3" />

                {/* Body */}
                <path d="M4 5v14c0 1.66 3.58 3 8 3s8-1.34 8-3V5" />

                {/* Middle lines */}
                <path d="M4 10c0 1.66 3.58 3 8 3s8-1.34 8-3" opacity="0.5" />
                <path d="M4 15c0 1.66 3.58 3 8 3s8-1.34 8-3" opacity="0.5" />
            </g>

            {/* Scan line */}
            {scanning && (
                <rect x="4" y="5" width="16" height="2" fill="#60a5fa" opacity="0.5" rx="1">
                    <animate
                        attributeName="y"
                        values="5;17;5"
                        dur="1.5s"
                        repeatCount="indefinite"
                    />
                </rect>
            )}
        </svg>
    );
};

/**
 * NetworkIcon - Clean network/graph icon
 */
export const NetworkIcon = ({
    size = 24,
    animated = false,
    className = ''
}) => {
    const id = React.useId();

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GoldGradient id={`${id}-gold`} />
                <GlowFilter id={`${id}-glow`} />
            </defs>

            <g filter={`url(#${id}-glow)`}>
                {/* Connections */}
                <g stroke="#D4AF37" strokeWidth="1" opacity="0.5">
                    <line x1="12" y1="12" x2="5" y2="5" />
                    <line x1="12" y1="12" x2="19" y2="5" />
                    <line x1="12" y1="12" x2="5" y2="19" />
                    <line x1="12" y1="12" x2="19" y2="19" />
                </g>

                {/* Outer nodes */}
                <circle cx="5" cy="5" r="2" fill="#60a5fa" />
                <circle cx="19" cy="5" r="2" fill="#34d399" />
                <circle cx="5" cy="19" r="2" fill="#60a5fa" />
                <circle cx="19" cy="19" r="2" fill="#34d399" />

                {/* Central node */}
                <circle
                    cx="12"
                    cy="12"
                    r="3"
                    fill={`url(#${id}-gold)`}
                    stroke="#FFD700"
                    strokeWidth="1"
                >
                    {animated && (
                        <animate
                            attributeName="r"
                            values="3;4;3"
                            dur="2s"
                            repeatCount="indefinite"
                        />
                    )}
                </circle>
            </g>
        </svg>
    );
};

/**
 * SearchIcon - Clean magnifying glass
 */
export const SearchIcon = ({
    size = 24,
    color = '#D4AF37',
    className = ''
}) => {
    const id = React.useId();

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GlowFilter id={`${id}-glow`} color={color} />
            </defs>

            <g filter={`url(#${id}-glow)`} stroke={color} strokeWidth="2" strokeLinecap="round">
                <circle cx="11" cy="11" r="7" fill="none" />
                <line x1="16" y1="16" x2="21" y2="21" />
            </g>
        </svg>
    );
};

/**
 * ExportIcon - Clean download/export icon
 */
export const ExportIcon = ({
    size = 24,
    color = '#D4AF37',
    className = ''
}) => {
    const id = React.useId();

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GlowFilter id={`${id}-glow`} color={color} />
            </defs>

            <g filter={`url(#${id}-glow)`} stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
            </g>
        </svg>
    );
};

/**
 * FilterIcon - Clean filter funnel
 */
export const FilterIcon = ({
    size = 24,
    color = '#D4AF37',
    active = false,
    className = ''
}) => {
    const id = React.useId();

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            className={className}
        >
            <defs>
                <GlowFilter id={`${id}-glow`} color={color} />
            </defs>

            <g filter={`url(#${id}-glow)`} stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" fill={active ? `${color}30` : 'none'} />
            </g>
        </svg>
    );
};

// Default export with all icons
export default {
    IluminateLogo,
    CompanyIcon,
    PersonIcon,
    LocationIcon,
    RiskIcon,
    VaultDoorIcon,
    StampIcon,
    DatabaseIcon,
    NetworkIcon,
    SearchIcon,
    ExportIcon,
    FilterIcon
};
