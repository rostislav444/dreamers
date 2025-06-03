import {
  Box,
  Container,
  Flex,
  SimpleGrid,
  Stack,
  Text,
  Heading,
  Link,
  Input,
  Button,
  HStack,
} from "@chakra-ui/react";
import NextLink from "next/link";
import React, { useState, useEffect } from "react";
import fetchApi from "@/utils/fetch";

// For this example, let's use simple Unicode icons
const PhoneIcon = () => <span style={{ fontSize: "1.2em" }}>📱</span>;
const EmailIcon = () => <span style={{ fontSize: "1.2em" }}>✉️</span>;
const LocationIcon = () => <span style={{ fontSize: "1.2em" }}>📍</span>;
const FacebookIcon = () => <span style={{ fontSize: "1.2em" }}>👤</span>;
const InstagramIcon = () => <span style={{ fontSize: "1.2em" }}>📷</span>;
const PinterestIcon = () => <span style={{ fontSize: "1.2em" }}>📌</span>;

interface LinkItemProps {
  name: string;
  href: string;
  slug?: string;
}

const SITE_LINKS: Array<LinkItemProps> = [
  { name: "Каталог", href: "/catalogue" },
  { name: "Про нас", href: "/about" },
  { name: "Доставка", href: "/delivery" },
  { name: "Оплата", href: "/payment" },
  { name: "Контакти", href: "/contacts" },
];

// This will be populated from the backend
const FALLBACK_CATEGORIES: Array<LinkItemProps> = [
  { name: "Столи", href: "/catalogue/tables" },
  { name: "Стільці", href: "/catalogue/chairs" },
  { name: "Дивани", href: "/catalogue/sofas" },
  { name: "Шафи", href: "/catalogue/wardrobes" },
  { name: "Ліжка", href: "/catalogue/beds" },
];

const ListHeader = ({ children }: { children: React.ReactNode }) => {
  return (
    <Text fontWeight="600" fontSize="lg" mb={4} color="brown.600">
      {children}
    </Text>
  );
};

// Simplified footer for server-side rendering
export const Footer = () => {
  return (
    <Box
      bg="brown.50"
      color="brown.600"
      borderTop="1px"
      borderColor="brown.100"
      mt={12}
      width="100%"
    >
      <Container as={Stack} maxW="container.full" py={10} px={{base: 4, sm: 6, md: 8, lg: 10}}>
        <SimpleGrid columns={{ base: 1, sm: 2, md: 4 }} spacing={8}>
          {/* Company info */}
          <Stack spacing={6}>
            <Box>
              <Text fontSize="xl" fontWeight="bold" color="brown.800">
                Dreamers ✨
              </Text>
              <Text fontSize="md" color="brown.500" fontWeight="medium" mt={1}>
                Меблі що надихають
              </Text>
            </Box>
            <Text fontSize="sm" color="brown.600">
              Ми створюємо меблі, які роблять життя комфортнішим. Дизайн та
              якість для вашого простору.
            </Text>
          </Stack>

          {/* Site Links */}
          <Stack align="flex-start">
            <ListHeader>Навігація</ListHeader>
            {SITE_LINKS.map((link) => (
              <Box key={link.name}>
                <Link
                  as={NextLink}
                  href={link.href}
                  color="brown.500"
                  _hover={{ color: "brown.700", textDecoration: "none" }}
                >
                  {link.name}
                </Link>
              </Box>
            ))}
          </Stack>

          {/* Contact info */}
          <Stack align="flex-start" spacing={4}>
            <ListHeader>Контакти</ListHeader>
            <HStack spacing={2}>
              <PhoneIcon />
              <Link href="tel:+380687426728" color="brown.500">
                +38 (068) 742-67-28
              </Link>
            </HStack>
            <HStack spacing={2}>
              <EmailIcon />
              <Link href="mailto:info@dreamers.com.ua" color="brown.500">
                info@dreamers.com.ua
              </Link>
            </HStack>
            <HStack spacing={2} align="flex-start">
              <Box pt={1}>
                <LocationIcon />
              </Box>
              <Text color="brown.600">
                вул. Київська 123,
                <br />
                м. Київ, 01001,
                <br />
                Україна
              </Text>
            </HStack>
          </Stack>
        </SimpleGrid>

        {/* Newsletter subscription */}
        <Box p={8} mt={8} borderRadius="xl" bg="brown.100">
          <SimpleGrid
            columns={{ base: 1, md: 2 }}
            spacing={8}
            alignItems="center"
          >
            <Box>
              <Heading as="h3" size="md" mb={2} color="brown.700">
                Підпишіться на новини та акції
              </Heading>
              <Text color="brown.600">
                Отримуйте інформацію про нові колекції та спеціальні пропозиції
              </Text>
            </Box>
            <Flex>
              <Input
                placeholder="Ваш email"
                bg="white"
                height="12"
                border={0}
                borderRadius="full"
                mr={2}
                _focus={{
                  boxShadow: "outline",
                }}
              />
              <Button
                bg="brown.500"
                px={8}
                height="12"
                color="white"
                _hover={{
                  bg: "brown.600",
                }}
                borderRadius="full"
              >
                Підписатися
              </Button>
            </Flex>
          </SimpleGrid>
        </Box>
      </Container>

      {/* Copyright and Legal */}
      <Box
        borderTopWidth={1}
        borderStyle="solid"
        borderColor="brown.100"
        bg="brown.500"
        color="white"
      >
        <Container
          as={Stack}
          maxW="container.full"
          py={4}
          px={12}
          direction={{ base: "column", md: "row" }}
          spacing={4}
          justify={{ base: "center", md: "space-between" }}
          align={{ base: "center", md: "center" }}
        >
          <Text fontSize="sm">© 2025 Dreamers. Всі права захищені.</Text>
          <Stack direction="row" spacing={6}>
            <Link href="/privacy" fontSize="sm">
              Політика конфіденційності
            </Link>
            <Link href="/terms" fontSize="sm">
              Умови використання
            </Link>
          </Stack>
        </Container>
      </Box>
    </Box>
  );
};
