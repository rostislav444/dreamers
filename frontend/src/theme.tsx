import {extendTheme} from "@chakra-ui/react"

// Update the global styles
const styles = {
    global: {
        "body": {
            "fontFamily": "Montserrat, sans-serif",
            "color": "brown.500",
            "fontWeight": '500',
            "bg": 'brown.50',
        },
        // "*": {
        //     "borderRadius": "0 !important",  // attempt to force all elements, but this may not work for all Chakra UI components
        // },
    },
}

// Add your color mode config
const config = {
    initialColorMode: "light",
    useSystemColorMode: false,
}

// Override the default theme components
const components = {
    Box: {
        baseStyle: {
            position: 'relative'
        }
    },
    Button: {
        // 1. We can update the base styles
        baseStyle: {
            fontWeight: '500',
            cursor: 'pointer',
            borderRadius: 0
        },
        variants: {
            solid: {
                bg: 'brown.500',
                color: 'white',
                fontSize: 'md',
                _hover: {
                    bg: 'yellow.300',
                    color: 'brown.500'
                },
                _active: {
                    bg: 'orange.400',
                    color: 'yellow.200'
                }
            },
            ghost: {
                _hover: {
                    bg: 'brown.200',
                    color: 'white'
                },
                _active: {
                    bg: 'orange.400',
                    color: 'yellow.200'
                }
            }

        },
        defaultProps: {
            variant: 'solid',
        },
    },
    Input: {
        baseStyle: {
            field: {
                borderRadius: 0,
                height: 14,
                fontWeight: 500,

            },
        },
        variants: {
            outline: {
                field: {
                    bg: 'white',
                    border: '2px solid',
                    borderColor: 'brown.500',
                    _focusVisible: {
                        borderColor: 'orange.500'
                    },
                    _hover: {
                        borderColor: 'orange.300'
                    },
                    _invalid: {
                        boxShadow: 'none',
                    }
                },
            },
        },
    },
    Textarea: {
        baseStyle: {
            borderRadius: 0,
            minHeight: 28,
            fontWeight: 500,
            pt: 4,

        },
        variants: {
            outline: {
                bg: 'white',
                border: '2px solid',
                borderColor: 'brown.500',
                _focusVisible: {
                    borderColor: 'orange.500'
                },
                _hover: {
                    borderColor: 'orange.300'
                }
            }
        }
    },
    Heading: {
        baseStyle: {
            fontWeight: 400,

        },
    },
    Divider: {
        baseStyle: {
            opacity: 1,
            borderColor: 'brown.500',
        }
    },
    Card: {
        baseStyle: {
            container: {
                backgroundColor: 'transparent',
                boxShadow: 'none',
                borderRadius: 0,
                color: 'brown.500',
                borderWidth: 4,
                borderColor: 'brown.500',
            }
        }
    }

}

const colors = {
    brown: {
        50: '#f5ebdc',
        100: '#eedfcd',
        200: '#cdaba6',
        300: '#da8d8d',
        400: '#a57c6c',
        500: '#8f2117',
        600: '#5f260e',
        700: '#421c0a',
        800: '#251206',
        900: '#080402',
    }
}


// Combine all configurations together
const theme = extendTheme({
    styles,
    colors,
    config,
    components,
})

export default theme;
