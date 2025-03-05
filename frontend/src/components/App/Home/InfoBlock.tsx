import { Box, Button, Heading, Text, VStack } from "@chakra-ui/react";
import Link from "next/link";
import { motion } from "framer-motion";

// Custom motion component
const MotionBox = motion(Box);

export interface InfoBlockProps {
  tagline: string;
  title: string;
  description: string;
  buttonText: string;
  buttonLink: string;
  delay?: number;
  bgColor?: string;
  textColor?: string;
  headingColor?: string;
  descriptionColor?: string;
  buttonVariant?: string;
  buttonColor?: string;
  buttonBorderColor?: string;
}

const InfoBlock = ({
  tagline,
  title,
  description,
  buttonText,
  buttonLink,
  delay = 0.2,
  bgColor = "brown.100",
  textColor = "brown.500",
  headingColor = "brown.500",
  descriptionColor = "brown.600",
  buttonVariant = "outline",
  buttonColor = "brown.500",
  buttonBorderColor = "brown.500",
}: InfoBlockProps) => {
  return (
    <MotionBox
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, delay }}
      borderRadius="xl"
      overflow="hidden"
      boxShadow="md"
      bg={bgColor}
      p={5}
      height="100%"
    >
      <VStack align="flex-start" height="100%" justify="center" spacing={4}>
        <Text
          fontSize="sm"
          textTransform="uppercase"
          fontWeight="medium"
          color={textColor}
        >
          {tagline}
        </Text>
        <Heading
          as="h2"
          fontSize={{ base: "xl", md: "2xl" }}
          fontWeight="medium"
          color={headingColor}
          lineHeight="shorter"
        >
          {title}
        </Heading>
        <Text color={descriptionColor} fontSize="md">
          {description}
        </Text>
        <Link href={buttonLink}>
          <Button
            size="sm"
            variant={buttonVariant}
            borderColor={buttonBorderColor}
            color={buttonColor}
            borderRadius="full"
            mt={2}
          >
            {buttonText}
          </Button>
        </Link>
      </VStack>
    </MotionBox>
  );
};

export default InfoBlock; 