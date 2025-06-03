import {
  Box,
  Button,
  Flex,
  Grid,
  Text,
  Container,
  VStack,
  HStack,
  AspectRatio,
  Heading,
  SimpleGrid,
} from "@chakra-ui/react";
import Link from "next/link";
import InspirationBlock from "@/components/App/Home/InspirationBlock";
import { CategoryState } from "@/interfaces/Categories";
import { ProductInterface } from "@/interfaces/Product";
import { ProductCard } from "@/components/App/Catalogue/ProductCard";
import { MEDIA_URL } from "@/local";
import { motion } from "framer-motion";
import InfoBlock from "@/components/App/Home/InfoBlock";
import FeaturedProductCard from "@/components/App/Home/FeaturedProductCard";

// Custom motion components
const MotionBox = motion(Box);
const MotionFlex = motion(Flex);
const MotionText = motion(Text);

interface Props {
  categories: CategoryState[];
  products: ProductInterface[];
}

const ResponsiveHero = ({ categories, products }: Props) => {
  // Make sure we have products before trying to split them
  const featuredProducts = products?.length ? products.slice(0, 4) : [];
  const restProducts = products?.length > 4 ? products.slice(4) : [];

  // Информационные блоки для отображения
  const infoBlocks = [
    {
      tagline: "Простір для мрій",
      title: "Меблі, що надихають на творчість",
      description: "Створіть простір, який відображає вашу індивідуальність та надихає на нові ідеї щодня",
      buttonText: "Відкрити колекцію",
      buttonLink: "/catalogue",
      bgColor: "brown.100",
      delay: 0.2
    }
  ];

  return (
    <Box width="100%" maxWidth="100vw">
      {/* Main Container with spacing */}
      <Container maxW="container.xl" py={6} px={{ base: 1, sm: 1, md: 1 }}>
        {/* Hero Grid Layout */}
        <Grid
          templateColumns={{ base: "1fr", lg: "1fr 1fr" }}
          templateRows={{
            base: "auto",
            lg: "1fr",
          }}
          gap={{ base: 4, md: 6 }}
          mb={{ base: 8, md: 10 }}
        >
          {/* Left Side - Main featured product */}
          <MotionBox
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            gridColumn={{ base: "1", lg: "1" }}
            gridRow={{ base: "1", lg: "1" }}
            borderRadius="xl"
            overflow="hidden"
            boxShadow="lg"
            height={{ base: "300px", md: "400px", lg: "100%" }}
            minHeight={{ lg: "500px" }}
          >
            {featuredProducts[0] && (
              <FeaturedProductCard
                product={featuredProducts[0]}
                isLarge={true}
              />
            )}
          </MotionBox>

          {/* Right Side - Grid of smaller items */}
          <Grid
            templateRows={{ base: "auto auto", md: "auto auto", lg: "1fr 1fr" }}
            templateColumns={{ base: "1fr", md: "1fr 1fr", lg: "1fr 1fr" }}
            gap={{ base: 4, md: 6 }}
            gridColumn={{ base: "1", lg: "2" }}
            gridRow={{ base: "2", lg: "1" }}
          >
            {/* Top left */}
            <MotionBox
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.1 }}
              gridRow="1"
              gridColumn={{ base: "1", md: "1" }}
              borderRadius="xl"
              overflow="hidden"
              boxShadow="md"
              position="relative"
              height={{ base: "200px", md: "250px", lg: "100%" }}
              minHeight={{ lg: "240px" }}
            >
              {categories[0] && (
                <Link href={`/catalogue/${categories[0].slug}`}>
                  <Box
                    position="relative"
                    height="100%"
                    transition="transform 0.3s ease"
                    _hover={{ transform: "scale(1.03)" }}
                  >
                    {categories[0].image.map((image, idx) => (
                      <Box
                        key={idx}
                        position="absolute"
                        top="0"
                        left="0"
                        width="100%"
                        height="100%"
                        backgroundImage={`url(${MEDIA_URL + image})`}
                        backgroundSize="cover"
                        backgroundPosition="center"
                      />
                    ))}
                    <Box
                      position="absolute"
                      bottom="0"
                      left="0"
                      width="100%"
                      bg="linear-gradient(to top, rgba(143, 33, 23, 0.7), transparent)"
                      p={4}
                      color="white"
                    >
                      <Heading as="h3" fontSize={{ base: "lg", md: "xl" }}>
                        {categories[0].name}
                      </Heading>
                    </Box>
                  </Box>
                </Link>
              )}
            </MotionBox>

            {/* Top right - InfoBlock */}
            <Box
              gridRow={{ base: "2", md: "1" }}
              gridColumn={{ base: "1", md: "2" }}
            >
              <InfoBlock {...infoBlocks[0]} />
            </Box>

            {/* Bottom left */}
            <MotionBox
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.3 }}
              gridRow={{ base: "3", md: "2" }}
              gridColumn={{ base: "1", md: "1" }}
              borderRadius="xl"
              overflow="hidden"
              boxShadow="md"
              position="relative"
              height={{ base: "200px", md: "250px", lg: "100%" }}
              minHeight={{ lg: "240px" }}
            >
              {featuredProducts[1] && (
                <FeaturedProductCard product={featuredProducts[1]} />
              )}
            </MotionBox>

            {/* Bottom right */}
            <MotionBox
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.4 }}
              gridRow={{ base: "4", md: "2" }}
              gridColumn={{ base: "1", md: "2" }}
              borderRadius="xl"
              overflow="hidden"
              boxShadow="md"
              position="relative"
              height={{ base: "200px", md: "250px", lg: "100%" }}
              minHeight={{ lg: "240px" }}
            >
              {featuredProducts[2] && (
                <FeaturedProductCard product={featuredProducts[2]} />
              )}
            </MotionBox>
          </Grid>
        </Grid>

        {/* Design Collections Section */}
        <Box mb={{ base: 12, md: 16 }} mt={{ base: 12, md: 16 }}>
          <MotionBox
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            mb={10}
          >
            <Flex
              justify="space-between"
              align="center"
              mb={6}
              direction={{ base: "column", sm: "row" }}
              gap={{ base: 3, sm: 0 }}
            >
              <Box>
                <Text
                  color="brown.500"
                  fontWeight="semibold"
                  fontSize="sm"
                  textTransform="uppercase"
                  mb={1}
                >
                  Наші колекції
                </Text>
                <Heading
                  fontSize={{ base: "2xl", md: "3xl" }}
                  fontWeight="medium"
                  color="brown.800"
                >
                  Каталог меблів
                </Heading>
              </Box>
              <Link href="/catalogue">
                <Button
                  variant="outline"
                  borderColor="brown.500"
                  color="brown.500"
                  borderRadius="full"
                  size="sm"
                >
                  Переглянути всі колекції
                </Button>
              </Link>
            </Flex>
          </MotionBox>

          {/* Collections Grid */}
          <SimpleGrid columns={{ base: 1, md: 3 }} spacing={{ base: 6, md: 8 }}>
            {categories.slice(0, 3).map((category, idx) => (
              <MotionBox
                key={category.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
              >
                <Box
                  borderRadius="xl"
                  overflow="hidden"
                  bg="brown.50"
                  boxShadow="md"
                  transition="all 0.3s ease"
                  _hover={{
                    transform: "translateY(-8px)",
                    boxShadow: "lg",
                  }}
                  height="100%"
                >
                  <AspectRatio ratio={4 / 3}>
                    <Box position="relative" width="100%" height="100%">
                      {category.image.map((image, idx) => (
                        <Box
                          key={idx}
                          position="absolute"
                          top="0"
                          left="0"
                          width="100%"
                          height="100%"
                          backgroundImage={`url(${MEDIA_URL + image})`}
                          backgroundSize="cover"
                          backgroundPosition="center"
                        />
                      ))}
                    </Box>
                  </AspectRatio>
                  <Box p={5}>
                    <Heading
                      fontSize="xl"
                      fontWeight="medium"
                      mb={2}
                      color="brown.700"
                    >
                      {category.name}
                    </Heading>
                    <Text color="brown.600" mb={3} fontSize="md">
                      {category.description ||
                        "Відкрийте для себе нашу прекрасну колекцію меблів"}
                    </Text>
                    <Link href={`/catalogue/${category.slug}`}>
                      <Button
                        variant="link"
                        color="brown.500"
                        fontWeight="medium"
                        size="sm"
                        rightIcon={
                          <Box as="span" ml={1}>
                            →
                          </Box>
                        }
                      >
                        Дізнатися більше
                      </Button>
                    </Link>
                  </Box>
                </Box>
              </MotionBox>
            ))}
          </SimpleGrid>
        </Box>

        {/* New Arrivals Section */}
        <Box mb={{ base: 12, md: 16 }}>
          <MotionBox
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            mb={10}
          >
            <Flex
              justify="space-between"
              align="center"
              direction={{ base: "column", sm: "row" }}
              gap={{ base: 3, sm: 0 }}
            >
              <Box>
                <Text
                  color="brown.500"
                  fontWeight="semibold"
                  fontSize="sm"
                  textTransform="uppercase"
                  mb={1}
                >
                  Останні надходження
                </Text>
                <Heading
                  fontSize={{ base: "2xl", md: "3xl" }}
                  fontWeight="medium"
                  color="brown.800"
                >
                  Нові надходження
                </Heading>
              </Box>
              <Link href="/catalogue?sort=newest">
                <Button
                  variant="outline"
                  borderColor="brown.500"
                  color="brown.500"
                  borderRadius="full"
                  size="sm"
                >
                  Переглянути всі новинки
                </Button>
              </Link>
            </Flex>
          </MotionBox>

          {/* Products Grid */}
          <SimpleGrid columns={{ base: 1, sm: 2, md: 4 }} spacing={{ base: 6, md: 8 }}>
            {restProducts.map((product, idx) => (
              <MotionBox
                key={product.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
              >
                <ProductCard product={product} />
              </MotionBox>
            ))}
          </SimpleGrid>
        </Box>
      </Container>

      {/* Inspiration Block - Full width */}
      <Box width="100%" overflow="hidden" mb={{ base: 12, md: 16 }}>
        <InspirationBlock />
      </Box>

      {/* Craftsmanship Section */}
      <Container maxW="container.xl" mb={{ base: 12, md: 16 }} px={{ base: 2, sm: 4, md: 6 }}>
        <SimpleGrid
          columns={{ base: 1, lg: 2 }}
          spacing={{ base: 6, md: 10 }}
          bg="brown.50"
          p={{ base: 6, md: 8 }}
          borderRadius="xl"
          boxShadow="md"
        >
          {/* Left side - Image */}
          <MotionBox
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <AspectRatio ratio={16 / 9} borderRadius="lg" overflow="hidden">
              <Box
                width="100%"
                height="100%"
                backgroundImage={`url("/craftsmanship.jpg")`}
                backgroundSize="cover"
                backgroundPosition="center"
              />
            </AspectRatio>
          </MotionBox>

          {/* Right side - Text */}
          <MotionBox
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <Text
              color="brown.500"
              fontWeight="semibold"
              fontSize="sm"
              textTransform="uppercase"
              mb={2}
            >
              Наш процес
            </Text>
            <Heading
              fontSize={{ base: "2xl", md: "3xl" }}
              fontWeight="medium"
              color="brown.800"
              mb={4}
            >
              Майстерність і якість
            </Heading>
            <Text
              fontSize={{ base: "md", md: "lg" }}
              color="brown.600"
              mb={6}
              lineHeight="tall"
            >
              Кожен виріб, який ми створюємо, поєднує в собі традиційну
              європейську майстерність із сучасним дизайном. Наші майстри
              забезпечують якість, яка залишається на покоління.
            </Text>

            {/* Process Steps */}
            <VStack spacing={4} align="flex-start">
              {[
                {
                  number: "01",
                  title: "Дизайн",
                  desc: "Продуманий дизайн, що поєднує естетику та функціональність",
                },
                {
                  number: "02",
                  title: "Підбір матеріалів",
                  desc: "Преміальні матеріали від надійних постачальників",
                },
                {
                  number: "03",
                  title: "Виробництво",
                  desc: "Досвідчені майстри створюють кожен виріб з точністю",
                },
              ].map((step) => (
                <HStack key={step.number} spacing={4} align="flex-start">
                  <Text fontWeight="bold" fontSize="xl" color="brown.400">
                    {step.number}
                  </Text>
                  <Box>
                    <Text
                      fontWeight="medium"
                      fontSize="lg"
                      color="brown.700"
                      mb={1}
                    >
                      {step.title}
                    </Text>
                    <Text color="brown.600">{step.desc}</Text>
                  </Box>
                </HStack>
              ))}
            </VStack>
          </MotionBox>
        </SimpleGrid>
      </Container>
    </Box>
  );
};

export default ResponsiveHero;
