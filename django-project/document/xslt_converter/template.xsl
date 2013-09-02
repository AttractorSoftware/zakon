<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">{#without html tag xsl work incorrect#}
        <html>
            <xsl:value-of select="document/description/place"/>
            <h1>
                <xsl:value-of select="document/description/name"/>
            </h1>
            <xsl:value-of select="document/description/revisions"/>
            <div id="contents">
                <xsl:choose>
                    <xsl:when test="//section">
                        <xsl:for-each select="//section">
                            <a href="#{@id}">
                                <xsl:value-of select="@name"/>
                            </a>
                            <br/>
                            <xsl:for-each select="./article">
                                <a href="#{@id}">
                                    <xsl:value-of select="@name"/>
                                </a>
                                <br/>
                            </xsl:for-each>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:for-each select="//article">
                            <a href="#{@id}">
                                <xsl:value-of select="@name"/>
                            </a>
                            <br/>
                        </xsl:for-each>
                    </xsl:otherwise>
                </xsl:choose>
            </div>
            <div id="content">
                <xsl:choose>
                    <xsl:when test="//section">
                        <xsl:for-each select="//section">
                            <div id="{@id}">
                                <h2>
                                    <xsl:value-of select="@name"/>
                                </h2>
                                <xsl:for-each select="./article">
                                    <div id="{@id}">
                                        <h3>
                                            <xsl:value-of select="@name"/>
                                        </h3>
                                        <xsl:choose>
                                            <xsl:when test="./item">
                                                <xsl:for-each select="./item">
                                                    <article id="{@id}"><xsl:value-of select="@number"/>.<xsl:value-of
                                                            select="."/>.
                                                    </article>
                                                    <br/>
                                                </xsl:for-each>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of select="."/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </div>
                                </xsl:for-each>
                            </div>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:for-each select="//article">
                            <div id="{@id}">
                                <h3>
                                    <xsl:value-of select="@name"/>
                                </h3>
                                <xsl:choose>
                                    <xsl:when test="./item">
                                        <xsl:for-each select="./item">


                                            <div class="article_id"><xsl:value-of select="@number"/>.
                                            </div>
                                            <article id="{@id}">
                                                <xsl:variable name="article_content" select="."/>

                                                <xsl:for-each select="reference">
                                                    -----
                                                </xsl:for-each>

                                                <xsl:value-of select="$article_content"/>
                                            </article>
                                            <br/>
                                        </xsl:for-each>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="."/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </div>
                        </xsl:for-each>
                    </xsl:otherwise>
                </xsl:choose>
            </div>
        </html>
    </xsl:template>
</xsl:stylesheet>