<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>

            <head>
                <meta charset="utf-8"/>
                <title>
                    <xsl:value-of select="document/description/name"/>
                </title>
                <link rel="stylesheet" type="text/css" href='../document/static/document/css/bootstrap.css'/>
            </head>

            <body>
                <div class="container" id="main">

                    <div class="description">
                        <h1 id="documentName">
                            <xsl:value-of select="document/description/name"/>
                        </h1>
                        <p id="place">
                            <xsl:value-of select="document/description/place"/>
                        </p>
                        <p id="date">
                            <xsl:value-of select="document/description/date"/>
                        </p>
                        <div class="revisions">
                            <article class="revision">

                                <div class="date">
                                    <p id="year">Год</p>
                                    <p>Месяц</p>
                                    <p>День</p>
                                </div>
                                <number>Номер</number>

                            </article>
                        </div>
                    </div>

                    <div id="contents">
                        <xsl:choose>
                            <xsl:when test="//section">
                                <xsl:for-each select="//section">
                                    <a href="#{@level}{@number}">
                                        <xsl:value-of select="@name"/>
                                    </a>
                                    <br/>
                                    <xsl:for-each select="./article">
                                        <a href="#article{@number}">
                                            <xsl:value-of select="@name"/>
                                        </a>
                                        <br/>
                                    </xsl:for-each>

                                </xsl:for-each>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:for-each select="//article">
                                    <a href="#article{@number}">
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
                                    <h2 id="{@level}{@number}">
                                        <xsl:value-of select="@name"/>
                                    </h2>
                                    <br/>

                                    <xsl:for-each select="./article">
                                        <h2 id="article{@number}">
                                            <xsl:value-of select="@name"/>
                                        </h2>
                                        <br/>

                                        <xsl:for-each select="./item">
                                            <article>
                                                <xsl:value-of select="@number"/>.
                                                <xsl:value-of select="."/>.
                                            </article>
                                            <br/>
                                        </xsl:for-each>

                                    </xsl:for-each>
                                </xsl:for-each>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:for-each select="//article">
                                    <h2 id="article{@number}">
                                        <xsl:value-of select="@name"/>
                                    </h2>
                                    <br/>

                                    <xsl:for-each select="./item">
                                        <article>
                                            <xsl:value-of select="."/>
                                        </article>
                                        <br/>
                                    </xsl:for-each>

                                </xsl:for-each>
                            </xsl:otherwise>
                        </xsl:choose>
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>