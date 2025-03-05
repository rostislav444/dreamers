import { Box, Text, Container, Divider, Flex, Heading, VStack, useBreakpointValue } from "@chakra-ui/react";
import { motion } from "framer-motion";

const MotionBox = motion(Box);
const MotionText = motion(Text);

const InspirationBlock = () => {
  return (
    <Box bg="brown.100" py={{ base: 12, md: 20 }} width="100%">
      <Container maxW="container.lg">
        <Flex 
          direction="column" 
          align="center" 
          textAlign="center"
          position="relative"
        >
          {/* Decorative elements */}
          <Box
            position="absolute"
            top={{ base: "-2rem", md: "-3rem" }}
            left="50%"
            transform="translateX(-50%)"
            fontSize={{ base: "5xl", md: "7xl" }}
            opacity={0.15}
            color="brown.500"
          >
            ✦
          </Box>
          
          <MotionBox
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
            mb={12}
          >
            <Text
              as="span"
              display="inline-block"
              color="brown.500"
              fontWeight="medium"
              fontSize={{ base: "sm", md: "md" }}
              textTransform="uppercase"
              letterSpacing="wider"
              mb={4}
            >
              Наша філософія
            </Text>
            
            <Heading
              as="h2"
              fontSize={{ base: "3xl", md: "4xl" }}
              fontWeight="medium"
              color="brown.700"
              letterSpacing="tight"
              lineHeight="1.2"
              mb={8}
            >
              Dreamers ✦ — Меблі що надихають
            </Heading>
          </MotionBox>
          
          {/* Decorative divider */}
          <MotionBox
            initial={{ opacity: 0, scaleX: 0 }}
            whileInView={{ opacity: 1, scaleX: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
            width="100px"
            mx="auto"
            mb={10}
          >
            <Divider borderColor="brown.500" borderWidth={1.5} />
          </MotionBox>
          
          {/* Main quote */}
          <MotionBox
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.4 }}
            maxW={{ base: "full", md: "3xl" }}
          >
            <Text
              fontSize={{ base: "xl", md: "2xl" }}
              fontWeight="light"
              color="brown.700"
              lineHeight="taller"
              letterSpacing="wide"
              mb={8}
            >
              &quot;Ми створюємо меблі, які роблять життя комфортнішим. Ми допомагаємо кожному клієнту знайти
              своє унікальне рішення, де дизайн та зручність створюють саме ваш простір для життя.&quot;
            </Text>
            
            <Text
              fontSize={{ base: "md", md: "lg" }}
              color="brown.600"
              maxW="2xl"
              mx="auto"
              lineHeight="tall"
            >
              Наші дизайнери черпають натхнення у європейській спадщині, водночас приймаючи сучасне бачення.
              Ми віримо у створення вічних предметів, які розповідають історію і розвиваються разом з вашим життям.
            </Text>
          </MotionBox>
        </Flex>
      </Container>
    </Box>
  );
};

export default InspirationBlock;