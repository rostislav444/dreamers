import Layout from "@/components/Shared/Layout";
import fetchApi from "@/utils/fetch";
import type { GetStaticProps } from "next";
import ResponsiveHero from "@/components/App/Home/ResponsiveHeroSection";
import { ProductInterface } from "@/interfaces/Product";
import { CategoryState } from "@/interfaces/Categories";

interface Props {
  categories: CategoryState[];
  products: ProductInterface[];
}

export default function Home({ categories, products }: Props) {
  return (
    <Layout
      breadcrumbs={[]}
      description="Dreamers | Меблі, що надихають"
      title="Dreamers | Меблі, що надихають"
    >
      <ResponsiveHero categories={categories} products={products} />
    </Layout>
  );
}

export const getStaticProps = (async (context) => {
  const api = fetchApi();
  const categoriesResp = await api.get("category", {}, true);
  // Get latest products by setting order parameter and page_size=8
  const productsResp = await api.get(
    "catalogue/products/",
    {
      page_size: 8,
      ordering: "-created_at", // Order by newest first (most recent creation date)
    },
    true,
  );

  return {
    props: {
      categories: categoriesResp.ok ? categoriesResp.data.results : [],
      products: productsResp.ok ? productsResp.data.results : [],
    },
    revalidate: 60 * 5, // Revalidate every 5 minutes
  };
}) satisfies GetStaticProps<{ categories: any; products: any }>;
