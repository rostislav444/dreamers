import {Box, Text, Container, Divider} from "@chakra-ui/react";

const InspirationBlock = () => {
    return (
        <Container maxW="4xl" py={32}>
            <Box textAlign="center" px={{base: 4, md: 12}} position="relative">
                {/* Декоративная звезда */}
                <Text
                    fontSize="6xl"
                    position="absolute"
                    top="-3rem"
                    left="50%"
                    transform="translateX(-50%)"
                    opacity={0.1}
                    color="brown.200"
                >
                    ✨
                </Text>

                {/* Слоган */}
                <Text
                    fontSize={{base: "2xl", md: "3xl", lg: "4xl"}}
                    fontWeight="medium"
                    color="brown.900"
                    mb={12}
                    letterSpacing="wide"
                >
                    Dreamers ✨ — меблі що надихають
                </Text>

                {/* Декоративный разделитель */}
                <Box maxW="24" mx="auto" mb={12}>
                    <Divider borderColor="brown.500" borderWidth={2}/>
                </Box>

                {/* Основной текст */}
                <Text
                    fontSize={{base: "lg", md: "xl", lg: "2xl"}}
                    fontWeight="normal"
                    color="brown.700"
                    lineHeight={{base: "tall", md: "taller"}}
                    letterSpacing="wide"
                >
                    Мис створюємо меблі, які роблять життя комфортнішим. Ми допомагаємо кожному клієнту знайти
                    своє унікальне рішення, де дизайн та зручність створюють саме ваш простір для життя.
                </Text>

            </Box>
        </Container>
    );
};

export default InspirationBlock;