from databaseClass import Database
from webscraperClass import WebScraper

if __name__ == "__main__":
    # Initialize Database
    db = Database()

    # Initialize WebScraper with the database object
    scraper = WebScraper(db)

        # List of website configurations
    website_configs = [
        # {
        #     "base_url": "https://silayipret.com",
        #     "collection_link_class": "header__menu-item header__menu-item--top list-menu__item focus-inset",
        #     "product_link_class": "full-unstyled-link",
        #     "product_name":"product__title",
        #     "price_class": "price__regular",
        #     "size_class": "js product-form__input variant-input-wrapper",
        #     "availability_class": "product-form__buttons",
        #     "description_class": "product__description rte",
        #     "image_class": "product__media image-animate media media--adapt media-mobile--adapt_first"
        # }
        # ,
        # {
        #     "base_url": "https://wearochre.com",
        #     "collection_link_class": "t4s-lh-1 t4s-d-flex t4s-align-items-center t4s-pr",
        #     "product_link_class": "t4s-full-width-link",
        #     "product_name":"t4s-product__info-container t4s-product__info-container--sticky",
        #     "price_class": "t4s-product-price",
        #     "size_class": "t4s-swatch__list",
        #     "availability_class": "t4s-btn-atc_text",
        #     "description_class": "t4s-product__description t4s-rte",
        #     "image_class": "t4s_ratio t4s-product__media"
        # }
        # ,
        # {
        #     "base_url": "https://www.noura.com.pk",
        #     "collection_link_class": "menu-drawer__menu-item list-menu__item link link--text focus-inset",
        #     "product_link_class": "full-unstyled-link",
        #     "product_name":"product__title",
        #     "price_class": "price__regular",
        #     "size_class": "js product-form__input product-form__input--pill",
        #     "availability_class": "product-form__buttons",
        #     "description_class": "product__description rte quick-add-hidden",
        #     "image_class": "product__media media media--transparent"
        # }
        # ,
        {
            "base_url": "https://www.kayseria.com",
            "collection_link_class": "site-nav-link m-zero link link--text focus-inset link-effect caption-large",
            "product_link_class": "card-link",
            "product_name":"productView-moreItem cust-title",
            "price_class": "price-item price-item--sale",
            "size_class": "js product-form__input clearfix",
            "availability_class": "product-form__buttons",
            "description_class": "productView-moreItem cust-desc",
            "image_class": "media"
        }
        # ,
        # {
        #     "base_url": "https://jazmin.pk",
        #     "collection_link_class": "header-sidebar__linklist-button h6 heading_all_caps_size",
        #     "product_link_class": "product-card__media",
        #     "product_name":"product-info__block-list",
        #     "price_class": "money",
        #     "size_class": "variant-picker__option v-stack gap-2 no-js:hidden",
        #     "availability_class": "button button--outline w-full",
        #     "description_class": "product-info__block-group accordion-group",
        #     "image_class": "product-gallery__media snap-center is-initial" 
        # }
            ]

    # Scrape multiple websites
    scraper.scrape_multiple_websites(website_configs)
    # scraper.db.save_product_details(["a", "b", "c", "d"])

    # Close the database connection when done
    db.close()
